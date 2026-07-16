# Autonomous Multi-Agent Market Intelligence & Content Pipeline

An end-to-end, zero-infrastructure DevOps pipeline that automates corporate trend-spotting and professional digital footprint management. Powered by a multi-agent orchestration framework, the system autonomously isolates high-impact corporate trends, generates strategic insights, and executes visual distribution pipelines entirely in the cloud.

## 🚀 Architecture Overview
1. **Dynamic Scraper (Trigger):** A lightweight API handler executes real-time indexing of breaking Indian technology, corporate, and macroeconomic trends.
2. **Agentic Layer (CrewAI + Groq):** 
   * **Market Research Analyst Agent:** Contextualizes unstructured web telemetry to extract underlying operational and strategic drivers.
   * **Content Strategist Agent:** Translates dense corporate data into polished narrative frameworks tailored for professional networks.
   * **Inference Engine:** Leverages highly optimized `Llama-3.3` models via Groq API for sub-second, token-efficient reasoning.
3. **Integration Layer (Make.com):** Intercepts payloads via live Webhooks, extracts contextual keywords, dynamically updates visual creative assets through image queries, and routes the final publication to social endpoints.
4. **DevOps & Infrastructure (GitHub Actions):** Hosted completely serverless, executing daily chron-schedules via CI/CD workflows without localized computational footprints.

## 🛠️ Tech Stack
* **Orchestration:** CrewAI Framework
* **Inference Pipeline:** Groq API / Llama-3.3
* **Live Telemetry:** Serper API (Google Search Engine Indexer)
* **Automation Backend:** Make.com / Serverless Webhooks
* **Media Asset Management:** Unsplash API Integration
* **CI/CD Execution:** GitHub Actions (Cron Scheduler / Ubuntu Workflow Containers)

## 📁 Repository Structure
```text
├── .github/
│   └── workflows/
│       └── schedule.yml    # CI/CD Cloud Automation Architecture
├── main.py                 # Core Script (Scraping, Agent Orchestration, Webhook Outbox)
├── requirements.txt        # Production-grade dependencies
└── README.md               # Project System Documentation
