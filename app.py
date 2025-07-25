import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

# Page configuration
st.set_page_config(page_title="Job Recommender", layout="wide")

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .main-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-bottom: 0;
    }
    
    /* File uploader styling */
    .upload-section {
        background: linear-gradient(145deg, #f8f9ff, #e8ecff);
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #667eea;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Analysis cards */
    .analysis-card {
        background: linear-gradient(145deg, #1e1e2e, #2d2d42);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        color: white;
        font-size: 16px;
        line-height: 1.6;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Job cards */
    .job-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 15px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 25px rgba(0,0,0,0.12);
    }
    
    .job-title {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .company-name {
        color: #667eea;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 0.8rem;
    }
    
    .job-details {
        color: #6c757d;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Success message styling */
    .success-message {
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">📄 AI Job Recommender</h1>
    <p class="main-subtitle">Upload your resume and get job recommendations based on your skills and experience from LinkedIn and Naukri.</p>
</div>
""", unsafe_allow_html=True)

# File uploader section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    with st.spinner("Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
    
    with st.spinner("Summarizing your resume..."):
        summary = ask_openai(f"Summarize this resume highlighting the skills, edcucation, and experience: \n\n{resume_text}", max_tokens=500)
        
    with st.spinner("Finding skill Gaps..."):
        gaps = ask_openai(f"Analyze this resume and highlight missing skills, certifications, and experiences needed for better job opportunities: \n\n{resume_text}", max_tokens=400)
    
    with st.spinner("Creating Future Roadmap..."):
        roadmap = ask_openai(f"Based on this resume, suggest a future roadmap to improve this person's career prospects (Skill to learn, certification needed, industry exposure): \n\n{resume_text}", max_tokens=400)
    
    # Display nicely formatted results
    st.markdown("---")
    st.markdown('<div class="section-header">📑 Resume Summary</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="analysis-card">{summary}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="section-header">🛠️ Skill Gaps & Missing Areas</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="analysis-card">{gaps}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="section-header">🚀 Future Roadmap & Preparation Strategy</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="analysis-card">{roadmap}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="success-message">✅ Analysis Completed Successfully!</div>', unsafe_allow_html=True)
    
    if st.button("🔎Get Job Recommendations"):
        with st.spinner("Fetching job recommendations..."):
            keywords = ask_openai(
                f"Based on this resume summary, suggest the best job titles and keywords for searching jobs. Give a comma-separated list only, no explanation.\n\nSummary: {summary}",
                max_tokens=100
            )
            
            search_keywords_clean = keywords.replace("\n", "").strip()
        
        st.success(f"Extracted Job Keywords: {search_keywords_clean}")
        
        with st.spinner("Fetching jobs from LinkedIn and Naukri..."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean, rows=60)
            naukri_jobs = fetch_naukri_jobs(search_keywords_clean, rows=60)
        
        st.markdown("---")
        st.markdown('<div class="section-header">💼 Top LinkedIn Jobs</div>', unsafe_allow_html=True)
        
        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"""
                <div class="job-card">
                    <div class="job-title">{job.get('title')}</div>
                    <div class="company-name">{job.get('companyName')}</div>
                    <div class="job-details">📍 {job.get('location')}</div>
                    <a href="{job.get('link')}" target="_blank" class="job-link">🔗 View Job</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No LinkedIn jobs found.")
        
        st.markdown("---")
        st.markdown('<div class="section-header">💼 Top Naukri Jobs (India)</div>', unsafe_allow_html=True)
        
        if naukri_jobs:
            for job in naukri_jobs:
                st.markdown(f"""
                <div class="job-card">
                    <div class="job-title">{job.get('title')}</div>
                    <div class="company-name">{job.get('companyName')}</div>
                    <div class="job-details">📍 {job.get('location')}</div>
                    <a href="{job.get('url')}" target="_blank" class="job-link">🔗 View Job</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No Naukri jobs found.")