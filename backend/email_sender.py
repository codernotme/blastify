import resend
import os
import time
from typing import List, Dict, Optional
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Configure Resend
resend.api_key = os.getenv("RESEND_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "Your Company <noreply@yourdomain.com>")

# Setup Jinja2 environment
template_dir = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(template_dir))

def render_email_body(name: str, message: str, template_name: str = "base_template.html") -> str:
    """
    Render email body using Jinja2 template
    
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
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Hello {name},</h2>
            <div>{message}</div>
            <br>
            <p>Best regards,<br>Your Company</p>
        </body>
        </html>
        """

def send_single_email(to_email: str, name: str, message: str, 
                     subject: str = "Your Personalized Message",
                     template_name: str = "base_template.html",
                     attachment: Optional[Dict] = None) -> Dict:
    """
    Send a single email using Resend API
    
    Args:
        to_email: Recipient email address
        name: Recipient name
        message: Email message content
        subject: Email subject line
        template_name: HTML template to use
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
        # Render email HTML
        html_content = render_email_body(name, message, template_name)
        
        # Prepare email data
        email_data = {
            "from": SENDER_EMAIL,
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

def send_bulk_emails(data: Dict, delay_seconds: int = 1, 
                    ab_test: bool = False) -> Dict:
    """
    Send bulk emails with optional A/B testing
    
    Args:
        data: Dictionary containing email data and settings
        delay_seconds: Delay between emails
        ab_test: Enable A/B testing with alternate subjects
        
    Returns:
        Dict: Results summary with individual email statuses
    """
    if not resend.api_key:
        return {
            "status": "error",
            "message": "Resend API key not configured",
            "results": []
        }
    
    # Extract data
    emails_data = data.get('emails', [])
    settings = data.get('settings', {})
    
    default_subject = settings.get('subject', 'Your Personalized Message')
    alt_subject = settings.get('alt_subject', 'Exclusive Offer Just for You')
    template_name = settings.get('template', 'base_template.html')
    
    results = []
    sent_count = 0
    failed_count = 0
    
    print(f"Starting bulk email send for {len(emails_data)} recipients...")
    
    for index, email_info in enumerate(emails_data):
        # Determine subject for A/B testing
        if ab_test and index % 2 == 0:
            subject = alt_subject
        else:
            subject = default_subject
        
        # Send email
        result = send_single_email(
            to_email=email_info.get('email'),
            name=email_info.get('name', 'Customer'),
            message=email_info.get('message', ''),
            subject=subject,
            template_name=template_name
        )
        
        results.append(result)
        
        # Update counters
        if result['status'] == 'sent':
            sent_count += 1
        else:
            failed_count += 1
        
        # Progress update
        print(f"Processed {index + 1}/{len(emails_data)}: {result['email']} -> {result['status']}")
        
        # Add delay between emails (except for the last one)
        if index < len(emails_data) - 1 and delay_seconds > 0:
            time.sleep(delay_seconds)
    
    # Return summary
    return {
        "status": "completed",
        "summary": {
            "total": len(emails_data),
            "sent": sent_count,
            "failed": failed_count,
            "success_rate": f"{(sent_count/len(emails_data)*100):.1f}%" if emails_data else "0%"
        },
        "results": results
    }

def send_bulk_emails_from_dataframe(df: pd.DataFrame, 
                                   subject: str = "Your Personalized Message",
                                   delay_seconds: int = 1,
                                   ab_test: bool = False,
                                   template_name: str = "base_template.html") -> Dict:
    """
    Send bulk emails from pandas DataFrame
    
    Args:
        df: DataFrame containing email data
        subject: Default subject line
        delay_seconds: Delay between emails
        ab_test: Enable A/B testing
        template_name: HTML template to use
        
    Returns:
        Dict: Results summary
    """
    # Convert DataFrame to dictionary format
    emails_data = []
    for _, row in df.iterrows():
        emails_data.append({
            'email': row.get('email'),
            'name': row.get('name', 'Customer'),
            'message': row.get('message', ''),
            'topic': row.get('topic', '')
        })
    
    data = {
        'emails': emails_data,
        'settings': {
            'subject': subject,
            'alt_subject': 'Exclusive Offer Just for You',
            'template': template_name
        }
    }
    
    return send_bulk_emails(data, delay_seconds, ab_test)

def test_resend_connection() -> Dict:
    """Test Resend API connection"""
    if not resend.api_key:
        return {"status": "error", "message": "Resend API key not configured"}
    
    try:
        # Try to send a test email to a validation endpoint
        test_result = send_single_email(
            to_email="test@resend.dev",  # Resend's test endpoint
            name="Test User",
            message="This is a test email to verify API connection.",
            subject="API Connection Test"
        )
        
        if test_result['status'] == 'sent':
            return {"status": "success", "message": "Resend API connection successful"}
        else:
            return {"status": "error", "message": f"Test email failed: {test_result.get('error')}"}
            
    except Exception as e:
        return {"status": "error", "message": f"Connection test failed: {str(e)}"}

def get_email_templates() -> List[str]:
    """Get list of available email templates"""
    try:
        template_files = []
        for filename in os.listdir(template_dir):
            if filename.endswith('.html'):
                template_files.append(filename)
        return template_files
    except Exception:
        return ["base_template.html"]  # Default fallback

def preview_email(name: str, message: str, template_name: str = "base_template.html") -> str:
    """Generate email preview HTML"""
    return render_email_body(name, message, template_name)
