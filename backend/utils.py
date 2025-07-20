import os
import re
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

def validate_email(email: str) -> bool:
    """
    Strict email validation - only accepts real, properly formatted emails
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    email = email.strip().lower()
    
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
    
    # More strict pattern matching
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False
    
    # Reject common fake/test domains
    fake_domains = {
        'test.com', 'example.com', 'test.test', 'fake.com', 'invalid.com',
        'dummy.com', 'sample.com', 'temp.com', 'placeholder.com',
        'test.org', 'example.org', 'fake.org', 'dummy.org'
    }
    
    domain_part = domain.lower()
    if domain_part in fake_domains:
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
    
    return True

def clean_email_list(emails: List[str]) -> List[str]:
    """
    Clean and validate a list of email addresses
    
    Args:
        emails: List of email addresses
        
    Returns:
        List[str]: Cleaned and validated email addresses
    """
    cleaned = []
    for email in emails:
        if isinstance(email, str):
            email = email.strip().lower()
            if validate_email(email):
                cleaned.append(email)
    return list(set(cleaned))  # Remove duplicates

def generate_subject_variations(base_subject: str) -> List[str]:
    """
    Generate subject line variations for A/B testing
    
    Args:
        base_subject: Base subject line
        
    Returns:
        List[str]: List of subject variations
    """
    variations = [base_subject]
    
    # Add some common variations
    if not base_subject.startswith('🎯'):
        variations.append(f"🎯 {base_subject}")
    
    if not base_subject.endswith('!'):
        variations.append(f"{base_subject}!")
    
    if 'exclusive' not in base_subject.lower():
        variations.append(f"Exclusive: {base_subject}")
    
    if 'limited time' not in base_subject.lower():
        variations.append(f"Limited Time: {base_subject}")
    
    return variations[:4]  # Return max 4 variations

def format_phone_number(phone: str) -> str:
    """
    Format phone number to a standard format
    
    Args:
        phone: Raw phone number
        
    Returns:
        str: Formatted phone number
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', str(phone))
    
    # Format based on length
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    sanitized = sanitized.strip('. ')
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return sanitized

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
        "estimated_completion": datetime.now().strftime('%H:%M:%S') if total_seconds < 3600 else "More than 1 hour"
    }

def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes
    
    Args:
        file_path: Path to file
        
    Returns:
        float: File size in MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return round(size_bytes / (1024 * 1024), 2)
    except OSError:
        return 0.0

def create_sample_csv() -> str:
    """
    Create a sample CSV file for user reference
    
    Returns:
        str: CSV content as string
    """
    sample_data = {
        'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown'],
        'email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'alice@example.com'],
        'topic': ['product launch', 'newsletter', 'special offer', 'event invitation'],
        'company': ['Tech Corp', 'Design Studio', 'Marketing Inc', 'Startup Hub']
    }
    
    df = pd.DataFrame(sample_data)
    return df.to_csv(index=False)

def validate_api_keys() -> Dict:
    """
    Validate that required API keys are configured
    
    Returns:
        Dict: Validation results
    """
    results = {
        "gemini": {"configured": bool(os.getenv("GEMINI_API_KEY")), "status": ""},
        "resend": {"configured": bool(os.getenv("RESEND_API_KEY")), "status": ""},
        "sender_email": {"configured": bool(os.getenv("SENDER_EMAIL")), "status": ""}
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
        "message": "All API keys configured" if all_configured else "Some API keys are missing"
    }

def create_error_report(errors: List[Dict]) -> str:
    """
    Create a formatted error report
    
    Args:
        errors: List of error dictionaries
        
    Returns:
        str: Formatted error report
    """
    if not errors:
        return "No errors to report."
    
    report = f"Error Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "=" * 50 + "\n\n"
    
    for i, error in enumerate(errors, 1):
        report += f"{i}. Email: {error.get('email', 'Unknown')}\n"
        report += f"   Status: {error.get('status', 'Unknown')}\n"
        report += f"   Error: {error.get('error', 'No error message')}\n"
        report += f"   Subject: {error.get('subject', 'Unknown')}\n\n"
    
    return report

def get_environment_info() -> Dict:
    """
    Get information about the current environment
    
    Returns:
        Dict: Environment information
    """
    return {
        "python_version": os.sys.version,
        "platform": os.name,
        "current_directory": os.getcwd(),
        "environment_variables": {
            "GEMINI_API_KEY": "***" if os.getenv("GEMINI_API_KEY") else "Not set",
            "RESEND_API_KEY": "***" if os.getenv("RESEND_API_KEY") else "Not set",
            "SENDER_EMAIL": os.getenv("SENDER_EMAIL", "Not set")
        }
    }
