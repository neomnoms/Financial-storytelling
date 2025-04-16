# 🧠 Financial Storytelling with AI

AI-powered analysis and visualization of Disney's 10-K financials using a localized Mistral 7B model and Google Cloud Platform.

---

## 📌 Project Overview

This project uses a locally hosted LLM (Mistral 7B via Ollama) to analyze Disney’s 10-K income statement and translate it into clear, human-friendly financial summaries. The goal is to make corporate financials easier to understand for non-experts while creating a reusable pipeline for future company reports.

---

## 🧠 Key Features

- Parse and process raw 10-K income statement data
- Summarize financial performance using LLM prompts
- Categorize line items into financial "buckets"
- Generate structured outputs for visualization
- Store and query data using Google Cloud (BigQuery & GCS)
- Visualize financial flow with Sankey diagrams

---

## 🛠️ Tech Stack

- **LLM**: Mistral 7B (via Ollama)
- **Interface**: OpenWebUI (for prompt testing)
- **Language**: Python (scripting, automation)
- **Storage & Querying**: Google Cloud Platform
  - BigQuery (structured data)
  - Cloud Storage (10-K files and outputs)
- **Visualization**: Plotly or Matplotlib (Sankey chart)
- **Version Control**: Git + GitHub

---

## 🗂️ Project Structure

data/ → 10-K files or cleaned CSVs
prompts/ → LLM prompt templates
scripts/ → Python scripts for automation
notebooks/ → Jupyter notebooks for development
outputs/ → LLM responses, visualization files
docker/ → Environment setup (optional)


---

## 🚀 Next Steps

- [x] Set up GitHub repo and folders ✅
- [x] Add prompt template for income statement
- [ ] Connect to GCP (BigQuery + GCS)
- [ ] Develop Mistral LLM pipeline
- [ ] Build visualization output (Sankey chart)
- [ ] Expand pipeline to support other companies

---

## 👩‍💻 Author

Naomi — AI student, data enthusiast, and financial storyteller 


