## 🤖 Intelligent Resume Optimization using LLM & Gemini Pro

This project is a Smart ATS Resume Analyzer that helps job seekers optimize their resumes for modern Applicant Tracking Systems (ATS) using Large Language Models and Google Gemini Pro. It compares a candidate’s resume with a target job description and provides clear, actionable feedback to increase interview shortlisting chances.[1]

### 🌟 Key Features

- **Resume–JD Match Score**  
  Calculates a percentage match between the resume and job description using semantic analysis rather than simple keyword matching.[1]

- **Missing Keyword Detection**  
  Identifies important skills and keywords required in the job description but missing or weak in the resume.[1]

- **AI-Powered Feedback**  
  Uses a Gemini-based LLM to generate easy-to-understand suggestions to improve summary, skills, and experience sections.[1]

- **Multi-format Resume Support**  
  Supports both PDF and DOCX file uploads for practical, real-world usage.[1]

- **Analytics Dashboard**  
  Stores evaluation results in CSV files and visualizes common skill gaps across multiple resumes for institutes, HR teams, and consultancies.[1]

- **User-Friendly Web App**  
  Built with Streamlit to provide a simple interface for uploading resumes, entering job descriptions, and viewing detailed results instantly.[1]

### 🛠 Tech Stack

- Python 3.10  
- Google Gemini Pro (Google Generative AI API)  
- Streamlit for web UI  
- PyMuPDF & `python-docx` for text extraction  
- Pandas & CSV for data storage and analytics[1]

### 🔁 Workflow

1. Upload a resume (PDF/DOCX).  
2. Paste the target job description.  
3. The system extracts and cleans text from the file.  
4. Resume and JD are sent to Gemini Pro for semantic analysis.  
5. The app displays match score, missing keywords, and detailed improvement suggestions, and logs results for analytics.

   
### 🚀 **Future Enhancements**
- Job portal auto-fetch (Naukri, LinkedIn)
- Mobile app (Android/iOS)
- ML-based hiring trend predictions
- LinkedIn profile optimization
- Enterprise bulk processing for colleges/HR

