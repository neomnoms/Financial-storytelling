import os
import json
from bs4 import BeautifulSoup

INPUT_FILE = 'data/raw_html/disney_10k_2024.html'
OUTPUT_FILE = 'data/parsed/disney_income_statement_2024.json'

def extract_income_statement(html_path):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    tables = soup.find_all('table')

    # Find the table with "Consolidated Statements of Income"
    target_table = None
    for table in tables:
        if "CONSOLIDATED STATEMENTS OF INCOME" in table.get_text().upper():
            target_table = table
            break

    if not target_table:
        raise ValueError("❌ Could not find the income statement table in the HTML.")

    rows = target_table.find_all('tr')
    income_data = {}

    for row in rows:
        cols = [col.get_text(strip=True).replace('\u00a0', ' ') for col in row.find_all(['td', 'th'])]
        if len(cols) >= 2:
            label = cols[0]
            value = cols[1].replace(',', '').replace('$', '')
            try:
                income_data[label] = int(value)
            except ValueError:
                continue  # Skip rows like "Earnings Per Share" or footnotes

    return income_data

def clean_and_save():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    print(f"📤 Extracting income statement from {INPUT_FILE}")
    try:
        income_data = extract_income_statement(INPUT_FILE)

        structured_json = {
            "company": "Disney",
            "year": 2024,
            "raw_statement": income_data  # Keep raw so you can categorize it later
        }

        with open(OUTPUT_FILE, 'w') as f:
            json.dump(structured_json, f, indent=2)
        print(f"✅ Cleaned income statement saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Error during extraction: {e}")

if __name__ == "__main__":
    clean_and_save()

