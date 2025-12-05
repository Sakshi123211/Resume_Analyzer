# 🎯 AI-Powered Resume Analyzer

An intelligent resume screening system that uses AI to automatically analyze resumes against job descriptions, providing match scores, visual insights, and automated email notifications for qualified candidates.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![Gemini AI](https://img.shields.io/badge/Gemini-AI-green.svg)
---
## 📸 Screenshots

### Main Interface
<img width="1918" height="887" alt="UI" src="https://github.com/user-attachments/assets/a61ca731-94f4-472c-bb9e-4b9cfe475d01" />


### Analysis Results
<img width="1623" height="791" alt="Analysis" src="https://github.com/user-attachments/assets/6234de1f-8751-440d-b580-fbe1e05db66b" />
<img width="1622" height="877" alt="analysis and summary" src="https://github.com/user-attachments/assets/02deebcd-182c-4a4d-af4f-a04b0ce41be4" />



### Email Notification
<img width="1495" height="730" alt="email" src="https://github.com/user-attachments/assets/52c668a3-6986-4eb9-a471-c616f7fa9ad1" />


---

## ✨ Features

- 📄 **PDF Resume Parsing** - Automatically extracts text from PDF resumes
- 🤖 **AI-Powered Analysis** - Uses Google Gemini AI for intelligent matching
- 📊 **Visual Analytics** - Interactive charts and gauges for easy interpretation
- 🎯 **Smart Scoring** - Generates match scores (0-100) based on JD requirements
- 📧 **Automated Notifications** - Sends email alerts for qualified candidates (score > 75)
- 🔍 **Skills Gap Analysis** - Identifies matching and missing skills
- 📝 **AI-Generated Summaries** - Provides detailed candidate evaluations
- 🚀 **Fast Processing** - Analyzes resumes in seconds
- 🔒 **Secure** - API keys stored safely in environment variables

---


### Main Interface
```
┌─────────────────────────────────────────┐
│        🎯 Resume Analyzer               │
├────────────────┬────────────────────────┤
│ Upload Resume  │  Job Description       │
│ [📄 PDF File]  │  [Text Area]           │
└────────────────┴────────────────────────┘
         [🔍 Analyze Button]
```

### Results Display
- **Score Gauge** - Visual speedometer showing match percentage
- **Candidate Card** - Name, email, experience, key skills
- **Skills Chart** - Bar comparison of matching vs missing skills
- **AI Summary** - Detailed analysis and recommendations

---

## 🛠️ Tech Stack

### Core Technologies
- **[Python 3.8+](https://www.python.org/)** - Programming language
- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[Google Gemini AI](https://ai.google.dev/)** - AI/ML for resume analysis
- **[n8n](https://n8n.io/)** - Workflow automation for emails

### Libraries
- **PyPDF2** - PDF text extraction
- **Plotly** - Interactive data visualizations
- **Requests** - HTTP requests to webhooks
- **python-dotenv** - Environment variable management

---

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
│  (Browser)  │
└──────┬──────┘
       │
       ↓
┌──────────────────────────────────────┐
│       Streamlit Web App              │
│  ┌────────────────────────────────┐  │
│  │  1. Upload Resume (PDF)        │  │
│  │  2. Enter Job Description      │  │
│  └────────────────────────────────┘  │
└──────┬───────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────┐
│         PyPDF2                       │
│   (Extract Text from PDF)            │
└──────┬───────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────┐
│      Google Gemini AI                │
│  • Analyze Resume vs JD              │
│  • Extract Candidate Info            │
│  • Calculate Match Score             │
│  • Generate Summary                  │
└──────┬───────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────┐
│          Plotly Charts               │
│  • Score Gauge (0-100)               │
│  • Skills Comparison Bar Chart       │
└──────┬───────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────┐
│           n8n Workflow               │
│  • Receive Candidate Data via Webhook│
│  • IF Node: Check Score > 75         │
│     └─> Yes → Trigger Gmail Node     │
│     └─> No  → Do nothing             │
└──────┬───────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────┐
│           Gmail                      │
│  (Send Notification Email)           │
└──────────────────────────────────────┘

```

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key
- n8n account (for email automation)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
N8N_WEBHOOK_URL=your_n8n_webhook_url_here
```

---

## ⚙️ Configuration

### 1. Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to `.env` file

### 2. Set Up n8n Workflow

#### Option A: n8n Cloud (Recommended)
1. Sign up at [n8n.io](https://n8n.io/)
2. Create a new workflow
3. Add **Webhook** node:
   - Method: POST
   - Path: `resume-analyzer`
4. Add **Gmail** node:
   - Connect your Gmail account
   - Configure email template (see below)
5. Connect: Webhook → Gmail
6. Activate workflow
7. Copy webhook URL to `.env` file

#### Email Template for Gmail Node
**Subject:**
```
Candidate Alert: {{ $json["body"]["name"] }} — Score {{ $json["body"]["score"] }}%
```

**Message:**
```
New Qualified Candidate Found!

{{ $json["body"]["name"] }}
Email: {{ $json["body"]["email"] }}
Score: {{ $json["body"]["score"] }}
Experience: {{ $json["body"]["experience"] }}
Key Skills: {{ $json["body"]["skills"] }}

Summary:{{ $json["body"]["summary"] }}

This email was sent automatically by Resume Analyzer.
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🚀 Usage

### Start the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Step-by-Step Guide

1. **Upload Resume**
   - Click "Upload PDF" button
   - Select candidate's resume (PDF format only)

2. **Enter Job Description**
   - Paste the complete job description in the text area
   - Include required skills, experience, and qualifications

3. **Analyze**
   - Click the "🔍 Analyze" button
   - Wait 5-10 seconds for AI processing

4. **View Results**
   - **Match Score** - See the overall compatibility (0-100)
   - **Candidate Info** - Name, email, experience, skills
   - **Visual Charts** - Interactive gauge and bar charts
   - **AI Summary** - Detailed analysis and recommendations

5. **Email Notification** (Automatic)
   - If score > 75, email is automatically sent
   - Check your Gmail inbox for notification

---

## 📁 Project Structure

```
resume-analyzer/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── .gitignore                 # Git ignore file
├── README.md                  # This file
│
├── temp/                      # Temporary storage for uploaded PDFs
│
└── venv/                      # Virtual environment (not in repo)
```

### File Descriptions

- **app.py** - Main application logic
  - PDF text extraction
  - Gemini AI integration
  - UI components and charts
  - n8n webhook integration

- **requirements.txt** - All Python package dependencies
  - streamlit==1.31.0
  - google-generativeai==0.3.2
  - PyPDF2==3.0.1
  - plotly==5.18.0
  - requests==2.31.0
  - python-dotenv==1.0.0

- **.env** - Sensitive configuration (not committed to Git)
  - API keys
  - Webhook URLs

---

## 🔬 How It Works

### 1. PDF Text Extraction
```python
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
```
Extracts all text from PDF resume page by page.

### 2. AI Analysis
```python
def analyze_with_gemini(resume_text, job_description):
    prompt = f"""Analyze this resume against the job description..."""
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return json.loads(response.text)
```
Sends resume and JD to Gemini AI for intelligent comparison.

### 3. Scoring Algorithm
Gemini AI evaluates based on:
- ✅ Required skills match
- ✅ Experience level alignment
- ✅ Educational background
- ✅ Industry relevance
- ✅ Job title compatibility

**Score Ranges:**
- 90-100: Perfect match, exceeds requirements
- 75-89: Strong match, meets most requirements
- 50-74: Moderate match, meets some requirements
- 25-49: Weak match, significant gaps
- 0-24: Poor match, does not meet requirements

### 4. Visualization
- **Gauge Chart** - Plotly indicator showing score with color zones
- **Bar Chart** - Comparison of matching vs missing skills

---

## 🙏 Acknowledgments

- **Google Gemini AI** - For powerful language understanding
- **Streamlit** - For making web app development easy
- **n8n** - For workflow automation capabilities
- **Plotly** - For beautiful interactive charts
- **PyPDF2** - For PDF processing functionality

---

## 📧 Contact

**Anas Shaikh** - 2002shaikhanass@gmail.com

---
