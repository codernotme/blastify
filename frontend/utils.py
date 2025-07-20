import httpx
import resend
import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
from typing import List, Dict, Optional
import time

load_dotenv()

# Configuration
resend.api_key = os.getenv("RESEND_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "Your Company <noreply@yourdomain.com>")

# Setup Jinja2 environment
template_dir = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(template_dir))

def get_industry_prompt(industry: str) -> str:
    """Get industry-specific prompt context for Gemini"""
    templates = {
        "Generic": "about your company and services",
        "Real Estate": "about new listings, market updates, and property opportunities",
        "E-commerce": "about new product launches, discounts, and shopping experiences",
        "Healthcare": "about wellness plans, appointment reminders, and health services",
        "Education": "about courses, admissions, webinars, and educational opportunities",
        "Technology": "about software updates, tech solutions, and digital innovations",
        "Finance": "about financial services, investment opportunities, and market insights",
        "Retail": "about sales, promotions, new arrivals, and exclusive offers"
    }
    return templates.get(industry, templates["Generic"])

def generate_messages_with_gemini(df: pd.DataFrame, tone: str, industry: str, enhance_options: List[str]) -> List[str]:
    """
    Generate personalized email messages using Gemini AI
    
    Args:
        df: DataFrame containing contact information
        tone: Email tone (formal, friendly, urgent, promotional)
        industry: Industry context
        enhance_options: List of enhancement options
        
    Returns:
        List[str]: Generated email messages
    """
    if not GEMINI_KEY:
        return ["Error: Gemini API key not configured"] * len(df)
    
    messages = []
    context = get_industry_prompt(industry)
    
    for index, row in df.iterrows():
        email = row.get('email', '')
        name = row.get('name', 'Customer')
        topic = row.get('topic', 'our latest offerings')
        company = row.get('company', '')
        
        # Build personalized prompt
        prompt = f"""
        Write a {tone.lower()} marketing email for {name} at {company if company else 'their company'} about {topic}.
        Context: {context}.
        
        Requirements:
        - Keep it concise and engaging (under 250 words)
        - Personalize for {name}
        - Make it professional yet approachable
        - Focus on value proposition
        """
        
        if "Emojis" in enhance_options:
            prompt += "\n- Include relevant emojis to make it more engaging"
        if "Call to Action" in enhance_options:
            prompt += "\n- Include a clear and compelling call-to-action"
        if "HTML formatting" in enhance_options:
            prompt += "\n- Use HTML formatting with <p>, <strong>, <em> tags for better structure"
        else:
            prompt += "\n- Use plain text format"
        
        try:
            response = httpx.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}",
                headers={"Content-Type": "application/json"},
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=30.0
            )
            
            if response.status_code == 200:
                content = response.json()['candidates'][0]['content']['parts'][0]['text']
                messages.append(content.strip())
            else:
                messages.append(f"Error generating message for {name}: HTTP {response.status_code}")
                
        except Exception as e:
            messages.append(f"Error generating message for {name}: {str(e)}")
        
        # Small delay to respect API limits
        time.sleep(0.5)
    
    return messages

def render_email_html(name: str, message: str, template_name: str = "base_template.html") -> str:
    """
    Render email content using HTML template
    
    Args:
        name: Recipient name
        message: Email message content
        template_name: Template file name
        
    Returns:
        str: Rendered HTML content
    """
    try:
        template = env.get_template(template_name)
        return template.render(name=name, message=message)
    except Exception as e:
        # Fallback to simple HTML if template fails
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: white; padding: 30px; border: 1px solid #ddd; }}
                .footer {{ background: #f8f9fa; padding: 20px; text-align: center; font-size: 14px; color: #666; border-radius: 0 0 8px 8px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Blastify</h1>
                </div>
                <div class="content">
                    <h2>Hello {name},</h2>
                    <div>{message}</div>
                </div>
                <div class="footer">
                    <p>Best regards,<br>Your Company Team</p>
                </div>
            </div>
        </body>
        </html>
        """

def send_email_with_resend(to_email: str, name: str, message: str, subject: str,
                          sender_name: str = "Your Company", 
                          sender_email: Optional[str] = None,
                          attachment: Optional[Dict] = None) -> Dict:
    """
    Send individual email using Resend API
    
    Args:
        to_email: Recipient email address
        name: Recipient name
        message: Email message content
        subject: Email subject line
        sender_name: Sender name
        sender_email: Sender email address
        attachment: Optional attachment data
        
    Returns:
        Dict: Send result with status and details
    """
    if not resend.api_key:
        return {
            "email": to_email,
            "status": "failed",
            "error": "Resend API key not configured"
        }
    
    try:
        # Use provided sender email or default
        from_email = sender_email or SENDER_EMAIL
        if sender_name and sender_name != "Your Company":
            from_email = f"{sender_name} <{sender_email or SENDER_EMAIL.split('<')[1].strip('>')}"
        
        # Render email HTML
        html_content = render_email_html(name, message)
        
        # Prepare email data
        email_data = {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_content,
        }
        
        # Add attachment if provided
        if attachment:
            email_data["attachments"] = [attachment]
        
        # Send email
        response = resend.Emails.send(email_data)
        
        return {
            "email": to_email,
            "status": "sent",
            "id": response.get('id'),
            "subject": subject
        }
        
    except Exception as e:
        return {
            "email": to_email,
            "status": "failed",
            "error": str(e),
            "subject": subject
        }

def validate_api_configuration() -> Dict:
    """
    Validate API configuration and return status
    
    Returns:
        Dict: Configuration status
    """
    results = {
        "gemini": {"configured": bool(GEMINI_KEY), "status": ""},
        "resend": {"configured": bool(resend.api_key), "status": ""},
        "sender_email": {"configured": bool(SENDER_EMAIL), "status": ""}
    }
    
    # Set status messages
    for service, info in results.items():
        if info["configured"]:
            info["status"] = "✅ Configured"
        else:
            info["status"] = "❌ Missing"
    
    all_configured = all(info["configured"] for info in results.values())
    
    return {
        "all_configured": all_configured,
        "services": results,
        "message": "All APIs configured" if all_configured else "Some API keys are missing"
    }

def create_sample_data() -> str:
    """
    Create sample CSV data for download
    
    Returns:
        str: CSV content as string
    """
    sample_data = {
        'name': [
            'John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Mike Wilson',
            'Sarah Davis', 'Tom Anderson', 'Lisa Garcia', 'David Martinez', 'Emma Thompson'
        ],
        'email': [
            'john.doe@example.com', 'jane.smith@example.com', 'bob.johnson@example.com',
            'alice.brown@example.com', 'mike.wilson@example.com', 'sarah.davis@example.com',
            'tom.anderson@example.com', 'lisa.garcia@example.com', 'david.martinez@example.com',
            'emma.thompson@example.com'
        ],
        'topic': [
            'product launch', 'newsletter subscription', 'special offer', 'event invitation',
            'service update', 'new features', 'customer survey', 'webinar invitation',
            'exclusive deal', 'company update'
        ],
        'company': [
            'Tech Corp', 'Design Studio', 'Marketing Inc', 'Startup Hub', 'Digital Agency',
            'Creative Solutions', 'Innovation Labs', 'Growth Partners', 'Future Systems', 'Smart Ventures'
        ]
    }
    
    df = pd.DataFrame(sample_data)
    return df.to_csv(index=False)

def estimate_send_time(num_emails: int, delay_seconds: int = 1) -> Dict:
    """
    Estimate time required to send bulk emails
    
    Args:
        num_emails: Number of emails to send
        delay_seconds: Delay between emails
        
    Returns:
        Dict: Time estimates
    """
    # Estimate processing time per email (including API call)
    processing_time_per_email = 2  # seconds
    
    total_seconds = (num_emails * processing_time_per_email) + ((num_emails - 1) * delay_seconds)
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return {
        "total_seconds": total_seconds,
        "formatted": f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}",
        "hours": int(hours),
        "minutes": int(minutes),
        "seconds": int(seconds)
    }

def test_email_connection(test_email: str = "test@resend.dev") -> Dict:
    """
    Test email sending capability
    
    Args:
        test_email: Test email address
        
    Returns:
        Dict: Test result
    """
    if not resend.api_key:
        return {"status": "error", "message": "Resend API key not configured"}
    
    try:
        result = send_email_with_resend(
            to_email=test_email,
            name="Test User",
            message="This is a test email to verify the email sending functionality.",
            subject="Blastify - Email System Test"
        )
        
        if result['status'] == 'sent':
            return {"status": "success", "message": "Email system test successful", "details": result}
        else:
            return {"status": "error", "message": f"Test failed: {result.get('error')}", "details": result}
            
    except Exception as e:
        return {"status": "error", "message": f"Test failed with exception: {str(e)}"}

def generate_subject_variations(base_subject: str) -> List[str]:
    """
    Generate subject line variations for A/B testing
    
    Args:
        base_subject: Base subject line
        
    Returns:
        List[str]: Subject variations
    """
    variations = [base_subject]
    
    # Add emoji variations
    if not any(emoji in base_subject for emoji in ['🎯', '📢', '🚀', '💡', '⭐']):
        variations.extend([
            f"🎯 {base_subject}",
            f"📢 {base_subject}",
            f"🚀 {base_subject}"
        ])
    
    # Add urgency variations
    if 'urgent' not in base_subject.lower() and 'limited' not in base_subject.lower():
        variations.extend([
            f"Urgent: {base_subject}",
            f"Limited Time: {base_subject}"
        ])
    
    # Add personalization variations
    variations.extend([
        f"Exclusive: {base_subject}",
        f"Just for You: {base_subject}"
    ])
    
    return variations[:6]  # Return max 6 variations

def export_results_to_csv(results: List[Dict]) -> str:
    """
    Export email sending results to CSV format
    
    Args:
        results: List of email sending results
        
    Returns:
        str: CSV content
    """
    df = pd.DataFrame(results)
    return df.to_csv(index=False)

def validate_email_list(df: pd.DataFrame) -> Dict:
    """
    Validate email list DataFrame with strict email checking
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Dict: Validation results
    """
    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "stats": {}
    }
    
    # Check required columns
    if 'email' not in df.columns:
        results["valid"] = False
        results["errors"].append("Missing required 'email' column")
    
    # Strict email validation
    if 'email' in df.columns:
        def validate_single_email(email):
            """Strict email validation function"""
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
            
            # Local part validation (before @)
            if not local or len(local) > 64:
                return False
            
            # Domain part validation (after @)
            if not domain or len(domain) > 255:
                return False
            
            # Domain must contain at least one dot
            if '.' not in domain:
                return False
            
            # Domain must not start or end with dot or hyphen
            if domain.startswith('.') or domain.endswith('.') or domain.startswith('-') or domain.endswith('-'):
                return False
            
            # Reject common fake/test domains
            fake_domains = {
                'test.com', 'example.com', 'test.test', 'fake.com', 'invalid.com',
                'dummy.com', 'sample.com', 'temp.com', 'placeholder.com',
                'test.org', 'example.org', 'fake.org', 'dummy.org'
            }
            
            if domain in fake_domains:
                return False
            
            # Domain must have valid TLD (at least 2 characters)
            domain_parts = domain.split('.')
            if len(domain_parts) < 2:
                return False
            
            tld = domain_parts[-1]
            if len(tld) < 2 or not tld.isalpha():
                return False
            
            # Check for consecutive dots or other invalid patterns
            if '..' in email or email.startswith('.') or email.endswith('.'):
                return False
            
            import re
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, email))
        
        valid_emails = df['email'].apply(validate_single_email)
        invalid_count = (~valid_emails).sum()
        
        if invalid_count > 0:
            results["warnings"].append(f"{invalid_count} invalid or fake email addresses found and will be filtered out")
    
    # Statistics
    results["stats"] = {
        "total_rows": len(df),
        "unique_emails": df['email'].nunique() if 'email' in df.columns else 0,
        "columns": list(df.columns),
        "missing_names": df['name'].isna().sum() if 'name' in df.columns else 0,
        "missing_messages": df['message'].isna().sum() if 'message' in df.columns else 0
    }
    
    return results
