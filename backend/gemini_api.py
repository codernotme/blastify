import httpx
import os
import asyncio
from typing import List, Dict
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def get_industry_prompt(industry: str) -> str:
    """Get industry-specific prompt context"""
    templates = {
        "Generic": "about your company and services",
        "Real Estate": "about new listings and market updates",
        "E-commerce": "about new product launches and discounts",
        "Healthcare": "about wellness plans and appointment reminders",
        "Education": "about courses, admissions, or webinars",
        "Technology": "about software updates and tech solutions",
        "Finance": "about financial services and investment opportunities",
        "Retail": "about sales, promotions, and new arrivals"
    }
    return templates.get(industry, templates["Generic"])

def generate_single_message(row: pd.Series, tone: str = "friendly", 
                          industry: str = "Generic", 
                          enhance_options: List[str] = None) -> str:
    """
    Generate a single email message using Gemini API
    
    Args:
        row: Pandas Series containing email data
        tone: Email tone (formal, friendly, urgent, promotional)
        industry: Industry context
        enhance_options: List of enhancement options
        
    Returns:
        str: Generated email content
    """
    if not GEMINI_API_KEY:
        return "Error: Gemini API key not configured"
    
    if enhance_options is None:
        enhance_options = []
    
    email = row.get('email', '')
    name = row.get('name', 'Customer')
    topic = row.get('topic', 'our latest offerings')
    context = get_industry_prompt(industry)
    
    # Build the prompt
    prompt = f"""
    Write a {tone.lower()} marketing email for {name} ({email}) about {topic}.
    Context: {context}.
    
    Requirements:
    - Keep it concise (under 200 words)
    - Personalize for {name}
    - Make it engaging and professional
    """
    
    if "Emojis" in enhance_options:
        prompt += "\n- Include relevant emojis"
    if "Call to Action" in enhance_options:
        prompt += "\n- Include a strong call-to-action"
    if "HTML formatting" in enhance_options:
        prompt += "\n- Format in clean HTML with proper styling"
    else:
        prompt += "\n- Use plain text format"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        response = httpx.post(
            f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
            json=payload,
            headers=headers,
            timeout=30.0
        )
        
        if response.status_code == 200:
            content = response.json()['candidates'][0]['content']['parts'][0]['text']
            return content.strip()
        else:
            return f"Error generating content: HTTP {response.status_code}"
            
    except Exception as e:
        return f"Error generating content for {email}: {str(e)}"

def generate_messages(df: pd.DataFrame, tone: str = "friendly", 
                     industry: str = "Generic", 
                     enhance_options: List[str] = None) -> List[str]:
    """
    Generate email messages for all rows in DataFrame
    
    Args:
        df: DataFrame containing email data
        tone: Email tone
        industry: Industry context
        enhance_options: List of enhancement options
        
    Returns:
        List[str]: Generated email messages
    """
    messages = []
    total_rows = len(df)
    
    print(f"Generating {total_rows} messages with Gemini API...")
    
    for index, row in df.iterrows():
        print(f"Processing {index + 1}/{total_rows}: {row.get('email', 'unknown')}")
        message = generate_single_message(row, tone, industry, enhance_options)
        messages.append(message)
        
        # Add small delay to respect API rate limits
        if index < total_rows - 1:  # Don't sleep after the last iteration
            import time
            time.sleep(0.5)
    
    return messages

async def generate_messages_async(df: pd.DataFrame, tone: str = "friendly", 
                                industry: str = "Generic", 
                                enhance_options: List[str] = None) -> List[str]:
    """
    Asynchronously generate email messages for better performance
    
    Args:
        df: DataFrame containing email data
        tone: Email tone
        industry: Industry context
        enhance_options: List of enhancement options
        
    Returns:
        List[str]: Generated email messages
    """
    if not GEMINI_API_KEY:
        return ["Error: Gemini API key not configured"] * len(df)
    
    if enhance_options is None:
        enhance_options = []
    
    async def generate_single_async(row: pd.Series) -> str:
        """Generate single message asynchronously"""
        email = row.get('email', '')
        name = row.get('name', 'Customer')
        topic = row.get('topic', 'our latest offerings')
        context = get_industry_prompt(industry)
        
        prompt = f"""
        Write a {tone.lower()} marketing email for {name} ({email}) about {topic}.
        Context: {context}.
        
        Requirements:
        - Keep it concise (under 200 words)
        - Personalize for {name}
        - Make it engaging and professional
        """
        
        if "Emojis" in enhance_options:
            prompt += "\n- Include relevant emojis"
        if "Call to Action" in enhance_options:
            prompt += "\n- Include a strong call-to-action"
        if "HTML formatting" in enhance_options:
            prompt += "\n- Format in clean HTML"
        
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    content = response.json()['candidates'][0]['content']['parts'][0]['text']
                    return content.strip()
                else:
                    return f"Error: HTTP {response.status_code}"
                    
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    # Generate all messages concurrently (with some rate limiting)
    tasks = []
    for _, row in df.iterrows():
        tasks.append(generate_single_async(row))
    
    # Process in batches to avoid overwhelming the API
    batch_size = 5
    results = []
    
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i + batch_size]
        batch_results = await asyncio.gather(*batch)
        results.extend(batch_results)
        
        # Small delay between batches
        if i + batch_size < len(tasks):
            await asyncio.sleep(1)
    
    return results

def test_gemini_connection() -> dict:
    """Test Gemini API connection and return status"""
    if not GEMINI_API_KEY:
        return {"status": "error", "message": "Gemini API key not configured"}
    
    test_prompt = "Write a short greeting email."
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{
                "text": test_prompt
            }]
        }]
    }
    
    try:
        response = httpx.post(
            f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
            json=payload,
            headers=headers,
            timeout=10.0
        )
        
        if response.status_code == 200:
            return {"status": "success", "message": "Gemini API connection successful"}
        else:
            return {"status": "error", "message": f"HTTP {response.status_code}: {response.text}"}
            
    except Exception as e:
        return {"status": "error", "message": f"Connection failed: {str(e)}"}
