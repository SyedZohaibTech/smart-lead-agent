# 🚀 S.Z Infinity — Autonomous B2B Lead Research & Outreach Agent

An AI-powered autonomous sales and research engine built to eliminate manual B2B prospecting. Given a company name and website URL (or a bulk CSV list), the agent scrapes live web content, identifies realistic operational bottlenecks, and generates hyper-personalized cold outreach emails.

🔗 **Live Demo:** [Launch Web App](https://smart-lead-agent-e7popujlnagq4xycfs777n.streamlit.app/)

---

## ✨ Key Features

- **Autonomous Web Scraping:** Extracts clean, structured business context from target company websites using `BeautifulSoup4` and `Requests`.
- **Bottleneck & Pain-Point Detection:** Uses Groq's ultra-fast LLM inference (`openai/gpt-oss-120b`) with strict JSON schema enforcement to analyze core business models and uncover growth bottlenecks.
- **Hyper-Personalized Pitch Generation:** Crafts tailored, non-generic cold emails aligned directly with the prospect's operational challenges.
- **Dual Execution Modes:**
  - **Single Lead Inspector:** Instant deep-dive research and email generation for individual prospects.
  - **Bulk CSV Processor:** Upload a CSV list of companies and export a complete outreach-ready spreadsheet in one click.

---

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **LLM Engine:** Groq API (`openai/gpt-oss-120b`)
- **Web Scraping:** BeautifulSoup4, Requests
- **Frontend & UI:** Streamlit
- **Data Processing:** Pandas

---

## ⚙️ Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/SyedZohaibTech/smart-lead-agent.git](https://github.com/SyedZohaibTech/smart-lead-agent.git)
   cd smart-lead-agent
2. Create and activate a virtual environment:
   python -m venv venv
    # Windows:
    venv\Scripts\activate
3. Install dependencies:
    pip install -r requirements.txt
4. Configure environment variables:
    Create a .env file in the root directory and add your Groq API key:
    Code snippet
    GROQ_API_KEY=your_groq_api_key_here
5. Run the application:
    Bash
    streamlit run app.py
👨‍💻 Author
Syed Zohaib — Founder & Agentic AI Engineer at S.Z Infinity Tech

📧 Contact: szinfinitysolutions@gmail.com
