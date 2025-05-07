import os
import json
import re
from typing import List, Dict
from ollama import Client

ollama = Client(host='http://localhost:11434')

INPUT_PATH = "data/parsed/disney_income_statement_2024.json"
OUTPUT_PATH = "data/parsed/disney_d3_ready_2024.json"


def build_prompt(company, year, raw_statement):
    return f"""
You are a financial storytelling assistant.

Your task is to examine the raw income statement below and group each line item into **5 to 7 high-level financial buckets**. Each bucket should represent a distinct category such as revenue, costs, taxes, or profit.

Use your reasoning to:
- Group similar items into top-level buckets (e.g., "Product Revenue", "Operating Expenses", "R&D", "Taxes", etc.)
- Do not break down categories into fine-grained sub-items unless absolutely necessary
- Structure a top-down money flow: income → costs → taxes → net profit
- Format your output for a Sankey diagram using "nodes" and "links"

🔒 Constraints (must follow all):
- Output ONLY a valid JSON object — no comments, no markdown, no explanation
- All "value" fields must be plain numeric literals (e.g., 1000000)
- Do NOT use negative values; reverse flow direction if needed
- The final node must be "Net Profit" or "Net Profit/Loss"
- Do NOT add additional fields such as "raw_statement"

🎯 Required format:
{{
  "company": "{company}",
  "year": {year},
  "nodes": [
    {{ "name": "X" }},
    {{ "name": "Y" }},
    ...
  ],
  "links": [
    {{ "source": 0, "target": 1, "value": 1230000 }}
  ]
}}

⚠️ Return only the raw JSON object. No headers. No footers. No markdown. 

Raw input: 
{json.dumps(raw_statement, indent=2)}
"""

def extract_json(response: str) -> Dict:
    match = re.search(r'({.*})', response, re.DOTALL)
    if not match:
        raise ValueError("❌ Could not extract a valid JSON structure from the response.")
    return json.loads(match.group(1))


def load_income_data(file_path: str) -> Dict:
    with open(file_path, 'r') as f:
        return json.load(f)


def save_json(data: Dict, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ AI-generated D3 flow structure saved to {output_path}")


def main():
    company = "Disney"
    year = 2024
    raw_statement = load_income_data(INPUT_PATH)
    prompt = build_prompt(company, year, raw_statement)

    print("🧠 Sending raw data for", company, "to Ollama...")
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        cleaned_json = extract_json(response['message']['content'])
        save_json(cleaned_json, OUTPUT_PATH)
    except ValueError as e:
        print(str(e))
        print("💥 Raw Ollama response was:\n", response['message']['content'])


if __name__ == "__main__":
    main()