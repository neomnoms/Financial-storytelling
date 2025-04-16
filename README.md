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

- **LLM Engine**: Mistral 7B (language model itself)
- **LLM Runner**: Ollama (runs LLM locally)
- **Prompt GUI**: OpenWebUI (for prompt testing)
- **Container**: Docker (only for GUI)
- **Language**: Python (scripting, automation)
- **Storage**: Google Cloud Platform
  - BigQuery (structured data)
  - Cloud Storage (10-K files and outputs)
- **Visualization**: Plotly or Matplotlib (TBDDDD)
- **Version Control**: Git + GitHub 

---

## 🧱 Full Project Tech Stack (Layered Architecture)

### 💻 Infrastructure Layer (Compute & Storage)
| Component     | Details                                                                 |
|---------------|-------------------------------------------------------------------------|
| RAM           | 8GB–24GB (depending on machine used for development/inference)         |
| CPU           | Intel/AMD CPU                                                           |
| GPU (optional)| Available on secondary machine for future fine-tuning or acceleration   |
| Storage       | Local SSD for development + Google Cloud Storage for project files      |

---

### 🗂️ Data Layer (Storage & Ingestion)
| Source / Tool                 | Purpose                                                 |
|------------------------------|----------------------------------------------------------|
| Local CSV / TXT files         | Income statement data, prompt templates, LLM outputs     |
| Google Cloud Storage (GCS)    | Backup and shared access to financial files              |
| Google BigQuery (planned)     | Structured query layer for financial records             |
| Google Trends (`pytrends`)    | Adds real-world public interest data for analysis        |

---

### 🧠 Machine Learning Layer (Model Inference & Analysis)
| Tool/Model     | Role                                                                |
|----------------|---------------------------------------------------------------------|
| Mistral 7B      | Local LLM for summarizing and explaining 10-K data                 |
| Ollama          | Local API interface and runtime for hosting LLMs                   |
| OpenWebUI       | Optional GUI interface for interacting with models (via Docker)    |
| Fine-tuning (future) | LoRA-based training to enhance financial domain specificity   |

---

### 💻 Application Layer (UI, API, Visualization)
| Tool/Framework     | Use Case                                                     |
|--------------------|--------------------------------------------------------------|
| Python Scripts      | Automate prompt loading, LLM inference, and file handling   |
| Jupyter Notebooks   | Exploration, testing, and rapid prototyping                 |
| GitHub              | Version control and project management                      |
| Plotly              | Sankey chart and future visualizations                      |
| Streamlit / Dash (planned) | Interactive dashboard or mini web app                |
| OpenWebUI (optional)| Local GUI for LLM prompt testing                            |
| ngrok (optional)    | Temporary public access to local web apps                   |


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

- [x] Set up GitHub repo and folders 
- [x] Add prompt template for income statement
- [ ] Connect to GCP (BigQuery + GCS)
- [x] Develop Mistral LLM pipeline
- [ ] Build visualization output (Sankey chart)
- [ ] Expand pipeline to support other companies


## Ideas 

- Benchmart against competitors (Disney vs Netflix)
- Fine-tune LLM on financial reports 
- Add a web scraper  
- Detect suspicious trends
- Implement Google Trends 


---

## 👩‍💻 Author

Naomi — AI student, data enthusiast, and financial storyteller 


