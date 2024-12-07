from twilio.rest import Client
import smtplib
import pandas as pd
from PyPDF2 import PdfReader
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
import math

def replace_nan(value):
    if isinstance(value, float) and math.isnan(value):
        return None
    return value

def is_valid_phone_number(phone_number):
    return re.match(r'^\+?\d{10,}$', phone_number) is not None

def extract_name(contact):
    # Assuming the name is in a field called 'name', otherwise adjust accordingly
    return contact.get('name', 'Unknown')

@api_view(['POST'])
def process_file(request):
    file = request.FILES.get('file')  # Get the uploaded file
    if not file:
        return Response({'error': 'No file uploaded'}, status=400)

    contacts = []
    if file.name.endswith('.xlsx') or file.name.endswith('.csv'):
        try:
            # Read the file and extract contact details
            df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
            contacts = df.to_dict(orient='records')  # Convert to dictionary
            contacts = [
                {k: replace_nan(v) for k, v in contact.items()}
                for contact in contacts if is_valid_phone_number(contact.get('phone number', ''))
            ]
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    elif file.name.endswith('.pdf'):
        try:
            # Read the PDF and extract text (simple extraction)
            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                # Assuming phone numbers and names are in the text, adjust extraction logic as needed
                for line in text.split('\n'):
                    if is_valid_phone_number(line):
                        contacts.append({'value': line, 'name': extract_name({'name': line})})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    else:
        return Response({'error': 'Unsupported file type'}, status=400)

    return Response({'contacts': contacts})

@api_view(['POST'])
def send_messages(request):
    data = request.data
    contacts = data.get('contacts', [])
    message = data.get('message', '')
    method = data.get('method', '')

    if not contacts or not message or not method:
        return Response({'error': 'Incomplete data'}, status=400)

    errors = []
    if method == 'email':
        for contact in contacts:
            try:
                send_email(contact['value'], message)
            except Exception as e:
                errors.append({'contact': contact, 'error': str(e)})
    elif method == 'whatsapp':
        for contact in contacts:
            try:
                send_whatsapp(contact['value'], message)
            except Exception as e:
                errors.append({'contact': contact, 'error': str(e)})

    if errors:
        return Response({'status': 'partial', 'errors': errors}, status=207)
    return Response({'status': 'success'})

def send_email(email, message):
    smtp_server = "smtp.example.com"
    smtp_port = 587
    smtp_user = "your_email@example.com"
    smtp_password = "your_password"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, email, message)

def send_whatsapp(phone_number, message):
    account_sid = "your_twilio_account_sid"
    auth_token = "your_twilio_auth_token"
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_="whatsapp:+14155238886",  # Twilio sandbox WhatsApp number
        to=f"whatsapp:{phone_number}"
    )