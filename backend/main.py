from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import PyPDF2  # Add import for PyPDF2
from typing import List  # Add import for List

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust based on frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure you have the required packages installed
# Run the following commands in your terminal:
# pip install fastapi
# pip install uvicorn

# Mock database for demonstration purposes
contacts_db = [
    {"id": "1", "name": "John Doe", "email": "john@example.com", "phone": "1234567890"},
    {"id": "2", "name": "Jane Smith", "email": "jane@example.com", "phone": "0987654321"},
    # Add more contacts as needed
]

@app.get("/contacts/", response_model=List[dict])
async def get_contacts():
    return contacts_db

@app.post("/process-file/")
async def process_file(file: UploadFile = File(...)):
    # Example for handling Excel files
    if file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        contacts = [{"name": row[0], "value": row[1]} for row in df.values]  # Assume names in the first column and contacts in the second column
        return {"contacts": contacts}
    # Add support for PDF files
    elif file.content_type == "application/pdf":
        contents = await file.read()
        reader = PyPDF2.PdfFileReader(io.BytesIO(contents))
        contacts = []
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text = page.extract_text()
            # Extract contacts from text (simple example, adjust as needed)
            for line in text.split('\n'):
                if "@" in line:  # Simple email detection
                    contacts.append({"name": "Unknown", "value": line.strip()})
        return {"contacts": contacts}
    return {"error": "Unsupported file format"}

@app.post("/send-messages/")
async def send_messages(
    contacts: list = Form(...), message: str = Form(...), method: str = Form(...)
):
    # Example logic for sending messages (you'll need real integration)
    if method == "email":
        status = f"Sent {len(contacts)} emails successfully."
    elif method == "whatsapp":
        status = f"Sent {len(contacts)} WhatsApp messages successfully."
    else:
        status = "Invalid method."
    return {"status": status}
