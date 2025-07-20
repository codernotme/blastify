from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import parser as file_parser, email_sender, gemini_api

load_dotenv()

app = FastAPI(title="Blastify Email Sender API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Blastify Email Sender API is running!"}

@app.post("/upload/")
async def upload_file(file: UploadFile, generate_from_gemini: bool = Form(False)):
    """Upload CSV/Excel file and optionally generate messages with Gemini"""
    try:
        df = file_parser.parse_file(file)
        
        if generate_from_gemini:
            df['message'] = gemini_api.generate_messages(df)
        
        return JSONResponse(content={"data": df.to_dict('records'), "status": "success"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/send-emails/")
async def send_bulk_emails(data: dict):
    """Send bulk emails using the provided data"""
    try:
        results = email_sender.send_bulk_emails(data)
        return JSONResponse(content=results)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/webhook/inbound-email/")
async def inbound_email(request: Request):
    """Handle inbound emails via Resend webhook"""
    try:
        payload = await request.json()
        # Log or store the email
        print(f"Received inbound email: {payload}")
        return {"status": "received"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
