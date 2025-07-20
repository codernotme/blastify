import streamlit as st
import pandas as pd
import time
import os
from typing import List, Dict
from io import BytesIO
import sys

# Add the current directory and parent directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

try:
    from utils import (
        generate_messages_with_gemini,
        render_email_html,
        send_email_with_resend,
        validate_api_configuration,
        create_sample_data,
        estimate_send_time
    )
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure all dependencies are installed and the utils module is available.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Blastify - Bulk Email Sender",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📧 Blastify - Bulk Email Sender</h1>
        <p>Your all-in-one solution for seamless bulk messaging with AI-powered content generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Configuration Check
        api_status = validate_api_configuration()
        if api_status["all_configured"]:
            st.success("✅ All APIs configured")
        else:
            st.error("❌ Missing API keys")
            st.info("Please check your .env file")
        
        st.markdown("---")
        
        # Email Settings
        st.subheader("📬 Email Settings")
        sender_name = st.text_input("Sender Name", value="Your Company")
        sender_email = st.text_input("Sender Email", value=os.getenv("SENDER_EMAIL", ""))
        
        # Generation Settings
        st.subheader("🧠 AI Generation")
        industry = st.selectbox(
            "Industry",
            ["Generic", "Real Estate", "E-commerce", "Healthcare", "Education", "Technology", "Finance", "Retail"]
        )
        tone = st.radio("Email Tone", ["Formal", "Friendly", "Urgent", "Promotional"])
        
        enhance_options = st.multiselect(
            "Enhance emails with:",
            ["Emojis", "HTML formatting", "Call to Action"],
            default=["HTML formatting"]
        )
        
        # Sending Settings
        st.subheader("🚀 Sending Options")
        ab_test = st.checkbox("📊 Enable A/B testing")
        schedule_delay = st.slider("⏱️ Delay between emails (seconds)", 0, 30, 3)
        
        # Download sample template
        if st.button("📥 Download Sample CSV"):
            sample_data = create_sample_data()
            st.download_button(
                label="💾 Download",
                data=sample_data,
                file_name="sample_email_list.csv",
                mime="text/csv"
            )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📤 Upload Email List")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload your contacts (CSV or Excel)",
            type=["csv", "xlsx", "xls"],
            help="File should contain at least an 'email' column. Optional columns: 'name', 'topic', 'company'"
        )
        
        # AI Generation toggle
        use_gemini = st.checkbox(
            "🧠 Auto-generate messages with Gemini AI",
            help="Generate personalized messages using AI based on recipient data"
        )
    
    with col2:
        st.header("📊 Quick Stats")
        if uploaded_file:
            try:
                # Load and display file info
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.metric("Total Contacts", len(df))
                if 'email' in df.columns:
                    valid_emails = df['email'].dropna().nunique()
                    st.metric("Unique Emails", valid_emails)
                
                # Time estimate
                time_est = estimate_send_time(len(df), schedule_delay)
                st.metric("Estimated Time", time_est["formatted"])
                
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    # Process uploaded file
    if uploaded_file:
        try:
            # Load data
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Validate required columns
            if 'email' not in df.columns:
                st.error("❌ Missing required 'email' column in the uploaded file.")
                st.stop()
            
            # Clean and validate data with strict email validation
            df['email'] = df['email'].astype(str).str.strip().str.lower()
            
            # Apply strict email validation - only real emails with '@' symbol
            def validate_strict_email(email):
                """Strict email validation - filters out fake/test emails"""
                if not email or not isinstance(email, str):
                    return False
                
                email = str(email).strip().lower()
                
                # Must contain exactly one @ symbol
                if email.count('@') != 1:
                    return False
                
                # Split into local and domain parts
                try:
                    local, domain = email.split('@')
                except ValueError:
                    return False
                
                # Basic validation
                if not local or not domain or '.' not in domain:
                    return False
                
                # Reject common fake/test domains
                fake_domains = {
                    'test.com', 'example.com', 'test.test', 'fake.com', 'invalid.com',
                    'dummy.com', 'sample.com', 'temp.com', 'placeholder.com',
                    'test.org', 'example.org', 'fake.org', 'dummy.org'
                }
                
                if domain in fake_domains:
                    return False
                
                # Domain must have valid TLD
                domain_parts = domain.split('.')
                if len(domain_parts) < 2:
                    return False
                
                tld = domain_parts[-1]
                if len(tld) < 2 or not tld.isalpha():
                    return False
                
                # Pattern validation
                import re
                pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                return bool(re.match(pattern, email))
            
            # Count original emails
            original_count = len(df)
            
            # Apply validation
            valid_emails = df['email'].apply(validate_strict_email)
            df = df[valid_emails]
            
            # Show filtering results
            filtered_count = original_count - len(df)
            if filtered_count > 0:
                st.warning(f"⚠️ Filtered out {filtered_count} invalid/fake email addresses. Only real emails with '@' symbol are accepted.")
            
            if df.empty:
                st.error("❌ No valid email addresses found in the file. Please ensure all emails are real and properly formatted with '@' symbol.")
                st.stop()
            
            # Fill missing columns
            if 'name' not in df.columns:
                df['name'] = 'Customer'
            if 'topic' not in df.columns:
                df['topic'] = 'our services'
            if 'message' not in df.columns:
                df['message'] = ''
            
            # Remove duplicates
            df = df.drop_duplicates(subset=['email'])
            
            st.success(f"✅ Successfully loaded {len(df)} unique contacts")
            
            # Generate messages with Gemini if requested
            if use_gemini and not df['message'].any():
                with st.spinner("🧠 Generating personalized messages with Gemini AI..."):
                    try:
                        messages = generate_messages_with_gemini(df, tone, industry, enhance_options)
                        df['message'] = messages
                        st.success("✅ Messages generated successfully!")
                    except Exception as e:
                        st.error(f"❌ Error generating messages: {str(e)}")
            
            # Display and edit data
            st.header("✏️ Review & Edit Your Email List")
            st.info("You can edit the data directly in the table below. Make sure all messages are complete before sending.")
            
            edited_df = st.data_editor(
                df,
                use_container_width=True,
                num_rows="dynamic",
                column_config={
                    "email": st.column_config.TextColumn("Email Address", width="medium"),
                    "name": st.column_config.TextColumn("Name", width="medium"),
                    "topic": st.column_config.TextColumn("Topic", width="medium"),
                    "message": st.column_config.TextColumn("Message", width="large")
                }
            )
            
            # Email Preview Section
            st.header("📬 Email Previews")
            
            # Select email to preview
            if len(edited_df) > 0:
                preview_index = st.selectbox("Select email to preview:", range(len(edited_df)), format_func=lambda x: f"{edited_df.iloc[x]['name']} ({edited_df.iloc[x]['email']})")
                
                if preview_index is not None:
                    row = edited_df.iloc[preview_index]
                    
                    # Subject line preview
                    if ab_test and preview_index % 2 == 0:
                        subject = "🎯 Exclusive Offer Just for You"
                    else:
                        subject = "📢 Important Update from Your Company"
                    
                    st.subheader(f"Preview for {row['name']}")
                    st.write(f"**To:** {row['email']}")
                    st.write(f"**Subject:** {subject}")
                    
                    # Render email HTML
                    try:
                        html_content = render_email_html(row['name'], row['message'])
                        st.components.v1.html(html_content, height=400, scrolling=True)
                    except Exception as e:
                        st.error(f"Error rendering email preview: {str(e)}")
            
            # Send emails section
            st.header("🚀 Send Emails")
            
            # Final confirmation
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Ready to Send", len(edited_df))
            with col2:
                st.metric("A/B Testing", "Enabled" if ab_test else "Disabled")
            with col3:
                st.metric("Delay", f"{schedule_delay}s")
            
            # Send button
            if st.button("🚀 Send All Emails", type="primary", use_container_width=True):
                if edited_df.empty:
                    st.error("❌ No emails to send!")
                elif edited_df['message'].isnull().any() or (edited_df['message'] == '').any():
                    st.error("❌ Some messages are empty. Please complete all messages before sending.")
                else:
                    send_bulk_emails(edited_df, ab_test, schedule_delay, sender_name, sender_email)
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
    
    else:
        # Show getting started info when no file is uploaded
        st.header("🚀 Getting Started")
        
        st.markdown("""
        <div class="info-box">
            <h3>📋 How to use Blastify:</h3>
            <ol>
                <li><strong>Prepare your email list:</strong> Create a CSV or Excel file with at least an 'email' column</li>
                <li><strong>Configure API keys:</strong> Add your Gemini and Resend API keys to the .env file</li>
                <li><strong>Upload your file:</strong> Use the file uploader above</li>
                <li><strong>Generate content:</strong> Let AI create personalized messages or write your own</li>
                <li><strong>Preview & send:</strong> Review your emails and send them with confidence</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample data format
        st.subheader("📄 Required File Format")
        sample_df = pd.DataFrame({
            'name': ['John Doe', 'Jane Smith'],
            'email': ['john@example.com', 'jane@example.com'],
            'topic': ['product launch', 'newsletter'],
            'company': ['Tech Corp', 'Design Studio']
        })
        st.dataframe(sample_df, use_container_width=True)
        
        st.info("💡 **Tip:** Use the 'Download Sample CSV' button in the sidebar to get a template file.")

def send_bulk_emails(df: pd.DataFrame, ab_test: bool, delay: int, sender_name: str, sender_email: str):
    """Send bulk emails with progress tracking"""
    
    st.subheader("📤 Sending Emails...")
    
    # Create progress bars
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Results tracking
    results = []
    sent_count = 0
    failed_count = 0
    
    # Create containers for live updates
    metrics_container = st.container()
    logs_container = st.container()
    
    with logs_container:
        log_placeholder = st.empty()
        log_messages = []
    
    try:
        total_emails = len(df)
        
        for index, row in df.iterrows():
            # Determine subject for A/B testing
            if ab_test and index % 2 == 0:
                subject = "🎯 Exclusive Offer Just for You"
            else:
                subject = "📢 Important Update from Your Company"
            
            # Update progress
            progress = (index + 1) / total_emails
            progress_bar.progress(progress)
            status_text.text(f"Sending to {row['email']} ({index + 1}/{total_emails})")
            
            # Send email
            try:
                result = send_email_with_resend(
                    to_email=row['email'],
                    name=row['name'],
                    message=row['message'],
                    subject=subject,
                    sender_name=sender_name,
                    sender_email=sender_email
                )
                
                results.append(result)
                
                if result['status'] == 'sent':
                    sent_count += 1
                    log_messages.append(f"✅ {row['email']} - Sent successfully")
                else:
                    failed_count += 1
                    log_messages.append(f"❌ {row['email']} - Failed: {result.get('error', 'Unknown error')}")
                
            except Exception as e:
                failed_count += 1
                error_msg = f"❌ {row['email']} - Error: {str(e)}"
                log_messages.append(error_msg)
                results.append({
                    'email': row['email'],
                    'status': 'failed',
                    'error': str(e)
                })
            
            # Update metrics
            with metrics_container:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Processed", index + 1)
                with col2:
                    st.metric("Sent", sent_count)
                with col3:
                    st.metric("Failed", failed_count)
                with col4:
                    success_rate = (sent_count / (index + 1)) * 100
                    st.metric("Success Rate", f"{success_rate:.1f}%")
            
            # Update logs (show last 10 messages)
            with log_placeholder.container():
                for msg in log_messages[-10:]:
                    st.text(msg)
            
            # Add delay between emails (except for the last one)
            if index < total_emails - 1 and delay > 0:
                time.sleep(delay)
        
        # Final results
        st.success(f"✅ Bulk email sending completed!")
        
        # Summary
        st.subheader("📊 Final Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Sent", sent_count, delta=sent_count)
        with col2:
            st.metric("Failed", failed_count, delta=-failed_count if failed_count > 0 else 0)
        with col3:
            final_rate = (sent_count / total_emails) * 100 if total_emails > 0 else 0
            st.metric("Success Rate", f"{final_rate:.1f}%")
        
        # Detailed results
        if failed_count > 0:
            st.subheader("❌ Failed Emails")
            failed_results = [r for r in results if r['status'] == 'failed']
            failed_df = pd.DataFrame(failed_results)
            st.dataframe(failed_df, use_container_width=True)
            
            # Download failed emails
            failed_csv = failed_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Failed Emails Report",
                data=failed_csv,
                file_name=f"failed_emails_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
    except Exception as e:
        st.error(f"❌ Critical error during bulk sending: {str(e)}")
    
    finally:
        progress_bar.progress(1.0)
        status_text.text("✅ Process completed!")

if __name__ == "__main__":
    main()
