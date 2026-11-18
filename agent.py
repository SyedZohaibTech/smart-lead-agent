import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Structured Output Schema (Taa ke data clean JSON mein mile)
class LeadOutreachPlan(BaseModel):
    company_summary: str = Field(description="Brief 2-line summary of what the company does")
    identified_pain_points: list[str] = Field(description="2-3 specific business or tech bottlenecks they might face")
    recommended_solution: str = Field(description="How AI or automation can solve their specific problem")
    cold_email_subject: str = Field(description="Catchy, non-spammy subject line")
    cold_email_body: str = Field(description="Personalized, concise cold email under 120 words")

def scrape_website(url: str) -> str:
    """Website se clean text extract karne ka tool"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Scripts aur styles hata dein
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
            
        text = soup.get_text(separator=' ')
        clean_text = ' '.join(text.split())
        return clean_text[:4000] # Token limit ke liye pehle 4000 characters
    except Exception as e:
        return f"Error scraping website: {str(e)}"

def run_lead_agent(company_name: str, website_url: str, your_service: str):
    print(f"\n🔍 Analyzing {company_name} ({website_url})...")
    site_content = scrape_website(website_url)
    
    if "Error scraping" in site_content:
        print(f"⚠️ {site_content}")
        return

    print("🧠 Thinking & identifying pain points...")
    
    prompt = f"""
    You are an elite B2B Sales & AI Solutions Strategist.
    Analyze the following website content for '{company_name}':
    
    --- WEBSITE CONTENT ---
    {site_content}
    -----------------------
    
    My Service/Agency Offer: {your_service}
    
    Task:
    1. Understand their core business.
    2. Identify 2-3 realistic operational or growth bottlenecks they likely face.
    3. Pitch my service naturally as a direct solution to those bottlenecks.
    4. Write a short, punchy, human-sounding cold email (NO generic fluff like "I hope this email finds you well").
    
    Respond STRICTLY in valid JSON matching this schema:
    {json.dumps(LeadOutreachPlan.model_json_schema())}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You output only valid JSON matching the requested schema."},
            {"role": "user", "content": prompt}
        ],
        model="openai/gpt-oss-120b",
        response_format={"type": "json_object"},
        temperature=0.4,
    )

    result = json.loads(chat_completion.choices[0].message.content)
    
    # Output Display
    print("\n" + "="*50)
    print(f"🏢 COMPANY: {company_name}")
    print("="*50)
    print(f"📌 Summary: {result['company_summary']}\n")
    print("🎯 Identified Pain Points:")
    for pt in result['identified_pain_points']:
        print(f"   - {pt}")
    print(f"\n💡 AI Angle: {result['recommended_solution']}\n")
    print("-" * 50)
    print(f"✉️  SUBJECT: {result['cold_email_subject']}")
    print("-" * 50)
    print(result['cold_email_body'])
    print("="*50 + "\n")

if __name__ == "__main__":
    # Test Run
    target_company = input("Target Company Name: ")
    target_url = input("Target Website URL (with https://): ")
    my_offer = "Custom AI Agents & Workflow Automation to cut manual operations by 60%"
    
    run_lead_agent(target_company, target_url, my_offer)