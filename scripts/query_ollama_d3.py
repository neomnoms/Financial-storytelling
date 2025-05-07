
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
You are a financial analyst creating a Sankey diagram to visualize how money flows through a company's operations.

You are working with structured income statement data for {company} for the year {year}.

Use your own reasoning to:
- Identify and extract distinct revenue streams (e.g., subscriptions, licensing, product sales, services, advertising, royalties, etc.)
- Identify major cost and expense categories (e.g., cost of goods sold, marketing, R&D, SG&A, legal, interest, taxes)
- Include government subsidies, tax credits, or incentives if present (e.g., energy credits, R&D tax breaks)
- Consolidate the data into meaningful buckets but avoid overly vague labels like “expenses” or “miscellaneous”

Format the output strictly as a valid JSON structure suitable for a D3.js Sankey diagram. Structure:
{{
  "company": "{company}",
  "year": {year},
  "nodes": [{{ "name": "Revenue Stream X" }}, ...],
  "links": [{{ "source": 0, "target": 1, "value": 1000000 }}, ...]
}}

🔁 Important constraints:
- All value fields must be positive.
- If an amount reduces another (like costs), reverse the source-target flow.
- Net Profit or Loss should always be the final node.
- All "value" fields must be numeric literals only — no text, variables, or expressions.
- Do not include explanations or commentary — only return the JSON block.


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
