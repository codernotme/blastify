# 🚀 Blastify - Bulk Email Sender

**Blastify** is your all-in-one solution for seamless bulk messaging with AI-powered content generation. Whether you're reaching out to customers, coordinating with a team, or sending announcements, Blastify makes communication faster, smarter, and more efficient.

## ✨ Key Features

- 📊 **Upload Email Lists** - CSV/Excel support with data validation
- 🧠 **AI-Powered Content** - Generate personalized messages using Gemini AI
- 📧 **Professional Templates** - Beautiful HTML email templates
- 🎯 **A/B Testing** - Test different subject lines for better engagement
- ⚡ **Bulk Sending** - Send thousands of emails with Resend API
- 📈 **Real-time Tracking** - Monitor sent/failed emails with detailed reporting
- 🎨 **Modern UI** - Clean Streamlit interface for easy management
- 🔧 **API Backend** - FastAPI server for advanced integrations

## 🏗️ Architecture

```
Frontend (Streamlit)
│
└──> Backend (FastAPI)
      ├── 📄 Email Parsing (CSV/Excel via Pandas)
      ├── 🧠 Gemini AI Integration
      ├── 📨 Resend API (Send & Receive)
      └── 🎨 HTML Email Templates
```

## 📂 Project Structure

```
blastify/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── email_sender.py      # Resend integration
│   ├── gemini_api.py        # AI content generation
│   ├── parser.py            # CSV/Excel processing
│   ├── utils.py             # Helper functions
│   └── templates/
│       └── base_template.html
├── frontend/
│   ├── app.py               # Streamlit application
│   ├── utils.py             # Frontend utilities
│   └── templates/
│       └── base_template.html
├── requirements.txt         # Python dependencies
├── run.py                  # Application runner
├── .env.template           # Environment variables template
└── README.md
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/codernotme/blastify.git
cd blastify
```

### 2. Setup the Application

```bash
python run.py setup
```

This will:
- Install all required dependencies
- Create a `.env` file from template
- Prepare the application for first run

### 3. Configure API Keys

Edit the `.env` file with your API keys:

```env
GEMINI_API_KEY=your-gemini-api-key-here
RESEND_API_KEY=your-resend-api-key-here
SENDER_EMAIL=Your Company <you@domain.com>
```

#### 🔑 Getting API Keys

**Gemini AI API:**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

**Resend API:**
1. Sign up at [Resend](https://resend.com)
2. Go to API Keys in your dashboard
3. Create a new API key
4. Copy the key to your `.env` file

### 4. Run the Application

```bash
python run.py streamlit
```

The application will start at `http://localhost:8501`

## 💡 Usage Guide

### 📤 Uploading Email Lists

1. **Prepare your CSV/Excel file** with these columns:
   - `email` (required) - Recipient email addresses
   - `name` (optional) - Recipient names
   - `topic` (optional) - Email topics for AI generation
   - `company` (optional) - Company names

2. **Example CSV format:**
   ```csv
   name,email,topic,company
   John Doe,john@example.com,product launch,Tech Corp
   Jane Smith,jane@example.com,newsletter,Design Studio
   ```

3. **Upload via the web interface** and review the data

### 🧠 AI Content Generation

1. **Enable AI generation** with the checkbox
2. **Select industry** and tone preferences
3. **Choose enhancements** (emojis, HTML formatting, CTA)
4. **Let Gemini AI** create personalized messages

### 📧 Email Customization

- **Edit messages** directly in the data editor
- **Preview emails** before sending
- **Customize templates** in the templates folder
- **Set sender information** in the sidebar

### 🚀 Sending Emails

1. **Configure sending options**:
   - Delay between emails (rate limiting)
   - A/B testing for subject lines
   - Sender name and email

2. **Review final settings** and email count
3. **Click "Send All Emails"** to start bulk sending
4. **Monitor progress** with real-time updates

## 🔧 Advanced Usage

### FastAPI Backend

Run the backend server separately for API access:

```bash
python run.py fastapi
```

API documentation available at `http://localhost:8000/docs`

### Custom Email Templates

1. Create new HTML templates in `backend/templates/` or `frontend/templates/`
2. Use Jinja2 syntax for dynamic content:
   ```html
   <h2>Hello {{ name }},</h2>
   <div>{{ message | safe }}</div>
   ```

### Batch Processing

For large email lists, the application automatically:
- Validates email addresses
- Removes duplicates
- Handles rate limiting
- Provides error reporting

## 📊 Features in Detail

### 🎯 A/B Testing
- Automatic subject line variations
- Performance tracking
- Statistical significance testing

### 📈 Analytics & Reporting
- Real-time sending progress
- Success/failure rates
- Detailed error logs
- Export capabilities

### 🔒 Security & Privacy
- Environment variable protection
- Email validation
- Rate limiting
- Error handling

## 🛠️ Development

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

```bash
black backend/ frontend/
flake8 backend/ frontend/
```

## 📝 API Reference

### Upload Endpoint
```http
POST /upload/
Content-Type: multipart/form-data

file: [CSV/Excel file]
generate_from_gemini: boolean
```

### Send Emails Endpoint
```http
POST /send-emails/
Content-Type: application/json

{
  "emails": [...],
  "settings": {...}
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/codernotme/blastify/issues)
- **Documentation**: This README and code comments
- **Email**: Create an issue for support requests

## 🚀 Roadmap

- [ ] Email scheduling
- [ ] Template marketplace
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Integration with CRM systems
- [ ] Mobile app

## ⚠️ Important Notes

- **Rate Limiting**: Resend has sending limits based on your plan
- **Email Validation**: Always validate your email lists
- **Compliance**: Ensure GDPR/CAN-SPAM compliance
- **Testing**: Test with small batches first

---

**Made with ❤️ by the Blastify Team**

*Blastify - Making bulk communication seamless, one message at a time.*
