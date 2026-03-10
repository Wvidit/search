# 🔍 Research Finder Agent

AI-powered agent that surfs the web using **Gemini 2.0 Flash** + **Google Search** to find top professors, PhD students, research labs, and internship opportunities in:

- **AI/ML integration in Materials Science** (specifically ceramics)  
- **Computer Vision** (interdisciplinary-friendly)

## ✨ Features

- 🌐 **Web-grounded AI search** — Uses Gemini with Google Search for real-time, accurate results
- 🎯 **Quality filters** — Only surfaces researchers from QS Top 100 universities / Stanford Top 2%
- 📧 **Contact details** — Emails, websites, Google Scholar profiles
- 🔬 **Project highlights** — Notable projects and recent publications
- 🏛️ **Lab discovery** — Renowned research labs with internship info
- 📋 **Internship links** — Direct application links for research internships
- 💾 **Export** — Download results as JSON or formatted text

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a free Gemini API key

Visit [Google AI Studio](https://aistudio.google.com/apikey) — no credit card required.

### 3. Run the app

```bash
streamlit run app.py
```

### 4. Search!

1. Enter your API key in the sidebar
2. Select search categories (all selected by default)
3. Click **🔍 Launch Search Agent**
4. Browse results across tabs
5. Export results as JSON or text

## 📁 Project Structure

```
finder-agent/
├── app.py              # Streamlit frontend (premium dark UI)
├── agent.py            # Core Gemini search agent
├── config.py           # Configuration & search categories
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md           # This file
```

## 🛠️ Tech Stack

- **Gemini 2.0 Flash** — Free-tier LLM with Google Search grounding
- **google-genai** — Official Google Gen AI Python SDK
- **Streamlit** — Modern Python web framework
- **Google Search** — Real-time web grounding for accurate results

## 📝 Notes

- Results are AI-generated and should be verified independently
- Contact details shown are only those publicly available
- The agent uses Gemini's free tier — rate limits may apply
