import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import os
import json
import csv
from datetime import datetime
from dotenv import load_dotenv
from helper import configure_genai, get_gemini_response, extract_pdf_text, extract_docx_text, prepare_prompt


def init_session_state():
    """Initialize session state variables."""
    if 'processing' not in st.session_state:
        st.session_state.processing = False


def save_analysis_record(resume_name, jd_match, missing_keywords):
    """Save analysis record to CSV for analytics."""
    try:
        record = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'resume_name': resume_name,
            'jd_match': jd_match,
            'missing_keywords_count': len(missing_keywords),
            'missing_keywords': ', '.join(missing_keywords[:5])  # Top 5
        }
        
        with open('analysis_records.csv', 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=record.keys())
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(record)
    except Exception as e:
        print(f"Error saving record: {str(e)}")


def show_analytics():
    """Display analytics dashboard."""
    st.title("📊 Analytics Dashboard")
    
    try:
        import pandas as pd
        df = pd.read_csv('analysis_records.csv')
        
        if df.empty:
            st.info("No analysis records yet. Start analyzing resumes to see insights!")
            return
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Analyses", len(df))
        with col2:
            avg_match = df['jd_match'].astype(str).str.rstrip('%').astype(float).mean()
            st.metric("Average JD Match", f"{avg_match:.1f}%")
        with col3:
            st.metric("Total Keywords Tracked", df['missing_keywords_count'].sum())
        
        # Match distribution
        st.subheader("JD Match Distribution")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        matches = df['jd_match'].astype(str).str.rstrip('%').astype(float)
        ax.hist(matches, bins=10, edgecolor='black', color='steelblue')
        ax.set_xlabel("JD Match %")
        ax.set_ylabel("Count")
        ax.set_title("Distribution of Match Scores")
        st.pyplot(fig)
        
        # Recent analyses
        st.subheader("Recent Analyses")
        st.dataframe(df.tail(10), use_container_width=True)
        
    except FileNotFoundError:
        st.info("No analytics data available yet.")


def main():
    # Load environment variables
    load_dotenv()

    # Initialize session state
    init_session_state()

    # Configure Generative AI
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Please set the GOOGLE_API_KEY in your .env file")
        return

    try:
        configure_genai(api_key)
    except Exception as e:
        st.error(f"Failed to configure API: {str(e)}")
        return

    # Sidebar Navigation
    with st.sidebar:
        st.title("🎯 OptiScore AI🚀")
        page = st.radio("Navigation", ["Resume Analyzer", "Analytics Dashboard"])
        st.divider()
        st.subheader("📋 About")
        st.write("""
        OptiScore AI Resume Analyzer helps you:
        - ✅ Upload PDF or DOCX resumes
        - ✅ Get instant analysis results
        - ✅ View match scores & improvements
        """)

    # Page Navigation
    if page == "Resume Analyzer":
        # Main content
        st.title("📄 OptiScore AI Resume Analyzer")
        st.subheader("Optimize Your Resume for ATS")

        # Input sections with validation
        jd = st.text_area(
            "Job Description",
            placeholder="Paste the job description here...",
            help="Enter the complete job description for accurate analysis"
        )

        uploaded_file = st.file_uploader(
            "Resume (PDF or DOCX)",
            type=["pdf", "docx"],
            help="Upload your resume in PDF or DOCX format"
        )

        # Process button with loading state
        if st.button("Analyze Resume", disabled=st.session_state.processing):
            if not jd:
                st.warning("Please provide a job description.")
                return

            if not uploaded_file:
                st.warning("Please upload a resume in PDF or DOCX format.")
                return

            st.session_state.processing = True

            try:
                with st.spinner("📊 Analyzing your resume..."):
                    # Extract text from resume (PDF or DOCX)
                    if uploaded_file.name.endswith('.pdf'):
                        resume_text = extract_pdf_text(uploaded_file)
                    elif uploaded_file.name.endswith('.docx'):
                        resume_text = extract_docx_text(uploaded_file)
                    else:
                        st.error("Unsupported file format. Please upload PDF or DOCX.")
                        st.session_state.processing = False
                        return

                    # Prepare prompt
                    input_prompt = prepare_prompt(resume_text, jd)

                    # Get and parse response
                    response = get_gemini_response(input_prompt)
                    response_json = json.loads(response)

                    # Display results
                    st.success("✨ Analysis Complete!")

                    # Match percentage
                    match_percentage = response_json.get("JD Match", "N/A")
                    st.metric("Match Score", match_percentage)

                    # Missing keywords
                    st.subheader("Missing Keywords")
                    missing_keywords = response_json.get("MissingKeywords", [])
                    if missing_keywords:
                        st.write(", ".join(missing_keywords))
                    else:
                        st.write("No critical missing keywords found!")

                    # Profile summary
                    st.subheader("Profile Summary")
                    st.write(response_json.get("Profile Summary", "No summary available"))

                    # Save record for analytics
                    save_analysis_record(uploaded_file.name, match_percentage, missing_keywords)

            except Exception as e:
                error_msg = str(e)
                if 'quota' in error_msg.lower() or '429' in error_msg:
                    st.error("⏳ Quota exceeded. Please wait 1 minute and try again, or upgrade your Gemini API plan for more requests.\n\nVisit: https://ai.google.dev/gemini-api/docs/rate-limits")
                else:
                    st.error(f"An error occurred: {error_msg}")

            finally:
                st.session_state.processing = False

    elif page == "Analytics Dashboard":
        show_analytics()


if __name__ == "__main__":
    main()
