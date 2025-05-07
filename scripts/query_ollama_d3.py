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

Your task is to examine the raw income statement data below and group each line item into logical financial buckets based on the company's income structure.

Use your own reasoning to:
- Identify and extract revenue streams (e.g., subscriptions, licensing, product sales, etc.)
- Identify and extract cost/expense categories (e.g., COGS, SG&A, R&D, marketing, legal, etc.)
- Include government subsidies or tax credits if present
- Map everything into a Sankey diagram-style format using nodes and links

Important constraints:

1. All "value" fields must be plain numbers only — use numeric literals (e.g., 5000000).
   - Never use text, labels, calculations, or variable names as values.

2. Do not use negative values. If an amount reduces another, reverse the direction of the flow instead.

3. The flow must go from income → expenses → taxes → net profit.
   - The last node must always be “Net Profit” or “Net Profit/Loss”.
   - Never flow *out of* the net profit node.

4. You must return only a valid raw JSON object.
   - Do not include any commentary, explanations, comments (e.g., // ...), markdown, or headings.
   - Do not use extra fields like "subtract" — only include "source", "target", and "value".
   - All values must be numeric literals only.
   - Output must start with { and end with } — no text before or after.

5. Structure must match this exactly:
{{
  "company": "{company}",
  "year": {year},
  "nodes": [{{ "name": "X" }}, {{ "name": "Y" }}],
  "links": [{{ "source": 0, "target": 1, "value": 5000000 }}]
}}

Here is the raw income data:
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