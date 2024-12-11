from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust based on frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-file/")
async def process_file(file: UploadFile = File(...)):
    # Example for handling Excel files
    if file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        contacts = [{"value": row[0]} for row in df.values]  # Assume contacts in the first column
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
