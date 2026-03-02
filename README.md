# 🤖 AI Job Search Agent - Portfolio Showcase

Welcome to the **AI Job Search Agent** showcase repository. This is a public demonstration of a private, autonomous system I built to streamline the job hunting process.

> **Note:** This repository is for demonstration purposes. The actual execution code, API keys, personalized prompts, and CV data are kept in a separate, private repository. The code provided here is a sanitized architectural example.

---

## 🏗️ Architecture & System Overview

The system acts as a personal "headhunter" that runs automatically on a schedule. It sweeps job boards, filters out "noise," deep-reads relevant job postings using AI, scores them against a given candidate profile, and even drafts tailored application documents.

### Key Components

| Component | Responsibility | Technology |
|-----------|----------------|------------|
| **1. Scraping Engine** | Finds new job listings based on defined keywords | `requests`, `BeautifulSoup` (for free HTML parsing) |
| **2. Pre-Filtering** | Fast, rule-based filtering (e.g., location matching and negative keyword blacklisting) | Python Regex & String matching |
| **3. Content Extraction** | Deep reading of full job descriptions for jobs that pass the pre-filter | **Firecrawl API** (Markdown conversion) |
| **4. AI Scoring** | Evaluates the job against the candidate's skills (e.g., Knowledge Management, AI Integration) | Weighted Keyword Analysis |
| **5. AI Ghostwriter** | Generates a tailored cover letter draft based on the scraped job text and a PDF CV | **Google Gemini API** (GenAI) |
| **6. Database & UI** | Tracks processed jobs to avoid duplicates and provides a frontend overview | **Supabase** (PostgreSQL), **Streamlit** |
| **7. Automation** | Orchestrates the entire pipeline on a schedule without manual intervention | macOS `LaunchAgent` / cron |

---

## 🚀 How It Works (The Pipeline)

```mermaid
graph TD;
    A[Scheduled Trigger (Cron/LaunchAgent)] --> B[Scraper Subsystem]
    B --> C{Passes Pre-Filter? (Location, Blacklist)}
    C -- No --> D[Discard / Log]
    C -- Yes --> E[Firecrawl API (Extract Full Text)]
    E --> F[Scoring & Categorization Engine]
    F --> G[Supabase DB (Save State)]
    G --> H[Fetcher Subsystem]
    H --> I[Gemini API (Draft Application with CV)]
    I --> J[Save Docs locally (Obsidian/Word)]
```

---

## 🛠️ Showcase Files

In the `src/` directory, you will find generic, sanitized excerpts of the real system to demonstrate the coding style and API integration logic:

1. **`scraper_demo.py`** - Demonstrates how the system handles HTTP requests, parses HTML with BeautifulSoup to save API credits, and uses the Firecrawl API to extract markdown from relevant postings.
2. **`filter_logic_demo.py`** - Shows the logic behind discarding irrelevant roles using word boundary regex, and assigning a match score based on positive/negative signals.
3. **`ai_writer_demo.py`** - A mock implementation of how the Gemini API generates the application texts using system instructions and PDF CV context.

---

## 💡 Why I Built This

Hunting for jobs manually involves sifting through hundreds of irrelevant postings. I built this autonomous pipeline to:
- **Save time:** Automate the repetitive search and first-draft process.
- **Showcase my skills:** Prove my ability to connect different APIs (Supabase, Firecrawl, Gemini) into a coherent, value-generating product.
- **Experiment with RAG & Prompts:** Iterate on how large language models handle context (like a CV) to generate highly specific texts without sounding generic.
