import streamlit as st
import google.generativeai as genai
import PyPDF2
import plotly.graph_objects as go
import requests
import json
import os


# Load secrets (works both locally and on Streamlit Cloud)
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    N8N_WEBHOOK_URL = st.secrets["N8N_WEBHOOK_URL"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# Configure Gemini with the working model
genai.configure(api_key=GEMINI_API_KEY)

# Page config
st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")


# Functions
def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def analyze_with_gemini(resume_text, job_description):
    """Use Gemini to analyze resume against JD"""

    prompt = f"""
Analyze this resume against the job description and respond ONLY with valid JSON (no markdown, no backticks).

Very important:
- Try your best to extract the candidate's FULL NAME from the header/contact section of the resume.
- Try your best to extract the candidate's EMAIL from the resume; do not invent one.
- If a field truly does not exist, return an empty string "" for that field, not "N/A".

Resume:
{resume_text}

Job Description:
{job_description}

Respond with this exact JSON format:
{{
  "score": <number 0-100>,
  "name": "<full candidate name or empty string>",
  "email": "<email address or empty string>",
  "experience": "<years/level, e.g. 'Fresher', '2-3 years', 'Senior'>",
  "skills": ["skill1", "skill2", "skill3"],
  "matching_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "summary": "<2-3 sentence summary>"
}}

Score: 75-100=Excellent, 50-74=Good, 0-49=Poor.
Return only JSON.
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    # Clean response
    response_text = response.text.strip()
    if response_text.startswith("```"):
        response_text = response_text.lstrip("`")
        if response_text.lower().startswith("json"):
            response_text = response_text[4:].lstrip()
        if response_text.endswith("```
            response_text = response_text[:-3].strip()

    data = json.loads(response_text.strip())

    # Post-process to avoid raw N/A
    name = data.get("name") or ""
    email = data.get("email") or ""
    if name.strip().upper() == "N/A":
        name = ""
    if email.strip().upper() == "N/A":
        email = ""

    data["name"] = name if name else "Unknown"
    data["email"] = email if email else "Unknown"

    return data


def create_score_gauge(score):
    """Create score gauge chart"""
    color = "green" if score >= 75 else "orange" if score >= 50 else "red"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x":, "y": },[3]
        title={"text": "Match Score", "font": {"size": 20}},
        gauge={
            "axis": {"range": },
            "bar": {"color": color},
            "steps": [
                {"range":, "color": "lightgray"},[4]
                {"range":, "color": "lightyellow"},[5][4]
                {"range":, "color": "lightgreen"},[5]
            ],
            "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 75},
        },
    ))
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10))
    return fig


def create_skills_chart(matching, missing):
    """Create skills comparison chart"""
    fig = go.Figure(data=[
        go.Bar(name="Matching", x=["Skills"], y=[len(matching)], marker_color="green"),
        go.Bar(name="Missing", x=["Skills"], y=[len(missing)], marker_color="red"),
    ])
    fig.update_layout(
        title="Skills Analysis",
        height=300,
        showlegend=True,
        barmode="group",
    )
    return fig


def send_to_n8n(data):
    """Send data to n8n webhook"""
    webhook_url = N8N_WEBHOOK_URL
    if webhook_url:
        try:
            response = requests.post(
                webhook_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            return 200 <= response.status_code < 300
        except Exception:
            return False
    return False


st.title("🎯 Resume Analyzer")
st.markdown("Upload resume PDF and enter job description to get AI-powered analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Resume")
    resume_file = st.file_uploader("Upload PDF", type=["pdf"])

with col2:
    st.subheader("💼 Job Description")
    job_desc = st.text_area("Paste JD here", height=150)

if st.button("🔍 Analyze", type="primary", use_container_width=True):
    if not resume_file:
        st.error("❌ Please upload a resume")
    elif not job_desc.strip():
        st.error("❌ Please enter job description")
    else:
        with st.spinner("🤖 Analyzing with Gemini AI..."):
            try:
                resume_text = extract_text_from_pdf(resume_file)
                results = analyze_with_gemini(resume_text, job_desc)

                # Debug once: see exactly what Gemini returned
                st.write("Gemini structured output:", results)

                st.success("✅ Analysis Complete!")
                st.markdown("---")
                st.header("📊 Results")

                col1, col2, col3 = st.columns()[6][3]

                with col1:
                    st.plotly_chart(create_score_gauge(results["score"]), use_container_width=True)

                with col2:
                    st.metric("Score", f"{results['score']}%")
                    if results["score"] >= 75:
                        st.success("✅ Excellent Match")
                    elif results["score"] >= 50:
                        st.warning("⚠️ Good Match")
                    else:
                        st.error("❌ Poor Match")

                with col3:
                    st.metric("Name", results["name"])
                    st.metric("Experience", results["experience"])

                st.subheader("👤 Candidate Details")
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**Email:** {results['email']}")
                    st.markdown(f"**Experience:** {results['experience']}")

                with col2:
                    st.markdown("**Top Skills:**")
                    for skill in results["skills"][:5]:
                        st.markdown(f"- {skill}")

                col1, col2 = st.columns(2)

                with col1:
                    st.plotly_chart(
                        create_skills_chart(results["matching_skills"], results["missing_skills"]),
                        use_container_width=True,
                    )

                with col2:
                    st.markdown("**✅ Matching Skills**")
                    for skill in results["matching_skills"][:5]:
                        st.markdown(f"- {skill}")

                    st.markdown("**❌ Missing Skills**")
                    for skill in results["missing_skills"][:5]:
                        st.markdown(f"- {skill}")

                st.subheader("📝 Summary")
                st.info(results["summary"])

                st.markdown("---")
                email_data = {
                    "name": results["name"],
                    "email": results["email"],
                    "score": results["score"],
                    "experience": results["experience"],
                    "skills": ", ".join(results["skills"][:5]),
                    "summary": results["summary"],
                }

                if send_to_n8n(email_data):
                    st.success("📊 Data sent to automation workflow!")
                else:
                    st.warning("⚠️ n8n webhook not configured or did not return 2xx")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with st.sidebar:
    st.header("")
    st.markdown("""
    **Score Guide:**
    - 75-100: Excellent Match ✅
    - 50-74: Good Match ⚠️
    - 0-49: Poor Match ❌

    **💡 Why Use Resume Analyzer?**
    - **Instant Comparison:** Quickly compares resumes against JD requirements.
    - **Highlights Key Skills & Experience:** Shows top candidate strengths at a glance.
    - **Saves Time:** Automates notifications for recruiters, reducing manual work.
    - **Data-Driven Hiring:** Makes hiring decisions precise and objective.
    """)

    st.markdown("---")
    st.markdown("**Status:**")
    if GEMINI_API_KEY:
        st.success("✅ Gemini API Connected")
    else:
        st.error("❌ Add GEMINI_API_KEY to secrets")

    if N8N_WEBHOOK_URL:
        st.success("✅ n8n Webhook Ready")
    else:
        st.warning("⚠️ Add N8N_WEBHOOK_URL to secrets")
