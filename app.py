import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="S.Z Infinity - AI Lead & Outreach Agent",
    page_icon="🚀",
    layout="wide"
)

# Custom Styling for Professional Look
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-text {
        color: #4B5563;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🚀 S.Z Infinity AI Lead & Outreach Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Autonomous B2B Lead Scraper, Pain Point Analyzer & Hyper-Personalized Pitch Generator</p>', unsafe_allow_html=True)

# Initialize Groq Client
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("⚠️ GROQ_API_KEY environment variable (.env) mein nahi mili! Pehle key configure karein.")
    st.stop()

client = Groq(api_key=api_key)

def scrape_website(url: str) -> str:
    """Extract clean text from target website"""
    try:
        if not url.startswith("http"):
            url = "https://" + url
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        text = soup.get_text(separator=' ')
        clean_text = ' '.join(text.split())
        return clean_text[:4000]
    except Exception as e:
        return f"Error scraping website: {str(e)}"

def analyze_lead(company_name: str, site_content: str, your_service: str) -> dict:
    """Call Groq API to analyze and generate outreach strategy"""
    prompt = f"""
    You are an elite B2B Sales & AI Solutions Strategist.
    Analyze the following website content for '{company_name}':
    
    --- WEBSITE CONTENT ---
    {site_content}
    -----------------------
    
    My Service/Agency Offer: {your_service}
    
    Task:
    1. Understand their core business (2-line summary).
    2. Identify 2-3 realistic operational or growth bottlenecks they likely face.
    3. Pitch my service naturally as a direct solution to those bottlenecks.
    4. Write a short, punchy, human-sounding cold email (NO generic fluff).
    
    Respond STRICTLY in valid JSON with these exact keys:
    - company_summary (string)
    - identified_pain_points (list of strings)
    - recommended_solution (string)
    - cold_email_subject (string)
    - cold_email_body (string)
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You output only valid JSON matching the requested keys."},
                {"role": "user", "content": prompt}
            ],
            model="openai/gpt-oss-120b",
            response_format={"type": "json_object"},
            temperature=0.4,
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

# Sidebar Controls
st.sidebar.header("⚙️ Configuration")
your_offer_input = st.sidebar.text_area(
    "Your Agency Offer / Service:",
    value="Custom AI Agents & Workflow Automation to cut manual operations by 60%"
)

app_mode = st.sidebar.selectbox("Choose Mode", ["Single Lead Inspector", "Bulk CSV Lead Processor"])

if app_mode == "Single Lead Inspector":
    col1, col2 = st.columns(2)
    with col1:
        company_input = st.text_input("Target Company Name", placeholder="e.g. Systems Limited")
    with col2:
        url_input = st.text_input("Website URL", placeholder="e.g. https://www.systemsltd.com")

    if st.button("🔍 Run Autonomous Research & Generate Pitch"):
        if not company_input or not url_input:
            st.warning("Please enter both Company Name and Website URL.")
        else:
            with st.spinner(f"Scraping {url_input} and analyzing with AI Agent..."):
                site_text = scrape_website(url_input)
                
                if "Error scraping" in site_text:
                    st.error(f"❌ {site_text}")
                else:
                    result = analyze_lead(company_input, site_text, your_offer_input)
                    
                    if "error" in result:
                        st.error(f"AI Error: {result['error']}")
                    else:
                        st.success("✅ Analysis Complete!")
                        
                        st.markdown("### 📌 Executive Summary")
                        st.write(result.get("company_summary"))
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown("### 🎯 Identified Bottlenecks")
                            for pt in result.get("identified_pain_points", []):
                                st.markdown(f"- {pt}")
                        with col_b:
                            st.markdown("### 💡 AI Automation Angle")
                            st.write(result.get("recommended_solution"))
                        
                        st.markdown("---")
                        st.markdown("### ✉️ Generated Cold Outreach Email")
                        st.text_input("Subject Line", value=result.get("cold_email_subject"))
                        st.text_area("Email Body", value=result.get("cold_email_body"), height=200)

elif app_mode == "Bulk CSV Lead Processor":
    st.markdown("### 📁 Upload Lead List (CSV)")
    st.markdown("CSV format mein do columns hone chahiye: `Company` aur `Website`.")
    
    # Sample CSV download option
    sample_df = pd.DataFrame({
        "Company": ["Systems Limited", "Daraz"],
        "Website": ["https://www.systemsltd.com", "https://www.daraz.pk"]
    })
    st.download_button(
        label="📥 Download Sample CSV Template",
        data=sample_df.to_csv(index=False).encode('utf-8'),
        file_name="sample_leads.csv",
        mime="text/csv"
    )

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded leads:", df.head())
        
        if st.button("🚀 Process All Leads Autonomousely"):
            results_list = []
            progress_bar = st.progress(0)
            total_rows = len(df)
            
            for index, row in df.iterrows():
                comp_name = row['Company']
                comp_url = row['Website']
                
                # Update progress
                progress_bar.progress((index + 1) / total_rows)
                
                site_text = scrape_website(comp_url)
                if "Error scraping" not in site_text:
                    res = analyze_lead(comp_name, site_text, your_offer_input)
                    if "error" not in res:
                        results_list.append({
                            "Company": comp_name,
                            "Website": comp_url,
                            "Summary": res.get("company_summary"),
                            "Pain_Points": "; ".join(res.get("identified_pain_points", [])),
                            "Email_Subject": res.get("cold_email_subject"),
                            "Email_Body": res.get("cold_email_body")
                        })
            
            if results_list:
                result_df = pd.DataFrame(results_list)
                st.success("🎉 All leads processed successfully!")
                st.dataframe(result_df)
                
                # Download result CSV
                st.download_button(
                    label="📥 Download Processed Outreach CSV",
                    data=result_df.to_csv(index=False).encode('utf-8'),
                    file_name="generated_outreach_leads.csv",
                    mime="text/csv"
                )