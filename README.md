# 📰 News Verification & Claim Analysis System

An agentic news verification system that analyzes news articles using multi-step reasoning instead of binary fake/real classification.

Given a news article URL, the system extracts factual claims, verifies them against multiple independent sources, analyzes bias and sensationalism, and produces a confidence-based assessment with clear explanations and uncertainty handling.

---

## 🎯 Project Motivation

Most existing fake news detection systems:

- Rely on black-box classifiers  
- Output only “fake” or “real” labels  
- Provide little or no explanation  

This project takes a different approach.

Instead of classification, it performs **claim-by-claim verification**, similar to how a human fact-checker or journalist would reason about a news article.

---

## 🧠 Core Idea

The system does **not** decide absolute truth.

It answers the question:

> “Based on available independent evidence, how confident can we be about each claim in this article?”

This makes the system:
- Explainable
- Conservative
- Realistic
- Suitable for real-world news analysis

---

## ⚙️ How the System Works

### 1. Article Scraping
- Fetches the article from the provided URL
- Removes ads, scripts, and navigation content
- Extracts clean readable article text

### 2. Claim Extraction
- Identifies only **verifiable factual claims**
- Ignores opinions, speculation, and emotional language
- Processes each claim independently

### 3. Entity Understanding
- Extracts important entities from each claim:
  - Person names
  - Locations
  - Country
  - Event type
- These entities are used to build meaningful search queries

### 4. Evidence Retrieval
- Performs entity-based web searches
- Uses multiple query variations to improve coverage
- Avoids generic or dictionary-style search results

### 5. Source Tiering
Each source is categorized into credibility tiers:

- **Tier 1** – International agencies (Reuters, AP, BBC, etc.)
- **Tier 2** – National or major regional media
- **Tier 3** – Local, niche, or regional outlets

Multiple independent Tier 3 sources can still support a claim, even if Tier 1 coverage is absent.

### 6. Claim Verification
For each claim, the system determines whether it is:

- supported  
- likely supported  
- inconclusive  
- contradicted  

Each decision is accompanied by a short explanation.

### 7. Bias & Sensationalism Analysis
- Analyzes the article’s language
- Detects emotional framing, exaggeration, or bias
- Bias is reported separately from factual correctness

### 8. Final Confidence Assessment
- Produces an overall confidence score (0–100)
- Explains why confidence is high, medium, or low
- Explicitly mentions missing or weak evidence

---

## 🧩 System Architecture

- **LangGraph** – Orchestrates the agentic workflow
- **LLM (via OpenRouter)** – Semantic reasoning and explanation
- **Deterministic Tools** – Web scraping, search, filtering
- **Streamlit** – Lightweight frontend for interaction

The system runs on CPU and does not train any machine learning models.

---

## 📁 Project Structure

news-verification-claim-analysis-system/
│

├── app.py # Streamlit frontend

├── main.py # Backend entry point

├── workflow.py # LangGraph workflow

│

├── agents.py # Reasoning agents

├── tools.py # Scraping & search utilities

├── utils.py # Logging & helpers

├── config.py # Configuration & environment variables

│

├── requirements.txt

├── .env.example

└── README.md

yaml
Copy code

---

## ▶️ How to Run the Project

### 1. Clone the repository
git clone https://github.com/your-username/news-verification-claim-analysis-system.git
cd news-verification-claim-analysis-system

### 2. Create and activate a virtual environment
python -m venv venv

Windows:
venv\Scripts\activate

Linux / macOS:
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Configure environment variables
Create a `.env` file using `.env.example`:

OPENROUTER_API_KEY=your_openrouter_api_key

### 5. Run the application
streamlit run app.py

---

## 🧪 Output

For each article, the system provides:

- Extracted factual claims
- Claim-by-claim verification results
- Supporting or contradicting sources
- Bias and sensationalism analysis
- Final confidence score with explanation

---

## ⚠️ Limitations

- Does not directly verify images or videos
- Depends on publicly indexed web sources
- Underreported events may remain inconclusive
- Designed for analysis, not absolute truth determination

These limitations are intentionally surfaced in the output.

---

