
import json
import subprocess
import re
import os

# Filepaths
JSON_INPUT = "data/parsed/disney_income_statement_2024.json"
JSON_OUTPUT = "data/parsed/disney_d3_ready_2024.json"

def load_raw_statement(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    company = data.get("company", "Unknown Company")
    year = data.get("year", "Unknown Year")
    raw_data = data.get("raw_statement", {})
    return company, year, raw_data

def build_prompt(company, year, raw_statement):
    return f"""
You are a financial storytelling assistant.

Your task is to examine the raw income statement data below and group each line item into logical financial buckets based on the company's income structure.

Use your own reasoning to:
- Create your own bucket categories (e.g., "Streaming Revenue", "Content Costs", "Administrative Expenses", "Taxes", etc.)
- Arrange the data into a top-down flow that represents the movement of money from income sources to profit/loss
- Format your output for a D3.js Sankey diagram using nodes and links.

💡 Please strictly follow this JSON structure:
```json
{{
  "company": "{company}",
  "year": {year},
  "nodes": [
    {{ "name": "Streaming Revenue" }},
    {{ "name": "Operating Costs" }},
    {{ "name": "Net Profit" }}
  ],
  "links": [
    {{ "source": 0, "target": 1, "value": 30000000 }},
    {{ "source": 1, "target": 2, "value": 15000000 }}
  ]
}}
```

⚠️ Only include the JSON code block — no explanations or extra formatting.

Here is the raw income data:
{json.dumps(raw_statement, indent=2)}
"""

def query_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode("utf-8")

def extract_json(response):
    try:
        match = re.search(r'```json\s*({.*?})\s*```', response, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except Exception as e:
        print("❌ Error parsing JSON:", e)
    return None

if __name__ == "__main__":
    company, year, raw_data = load_raw_statement(JSON_INPUT)
    print(f"🧠 Sending raw data for {company} ({year}) to Ollama...")

    prompt = build_prompt(company, year, raw_data)
    response = query_ollama(prompt)

    print("\n📤 Ollama's Response:\n")
    print(response)

    structured_json = extract_json(response)
    if structured_json:
        os.makedirs(os.path.dirname(JSON_OUTPUT), exist_ok=True)
        with open(JSON_OUTPUT, "w") as f:
            json.dump(structured_json, f, indent=2)
        print(f"\n✅ AI-generated D3 flow structure saved to {JSON_OUTPUT}")
    else:
        print("❌ Could not extract a valid JSON structure.")
