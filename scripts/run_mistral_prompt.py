# scripts/run_mistral_prompt.py

import ollama
from datetime import datetime

def load_prompt(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def run_mistral(prompt_text):
    response = ollama.chat(
        model='mistral',
        messages=[
            {"role": "system", "content": "You are a helpful financial analyst AI."},
            {"role": "user", "content": prompt_text}
        ]
    )
    return response['message']['content']

def save_output(output_text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"outputs/mistral_response_{timestamp}.txt"
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(output_text)
    print(f"✅ Output saved to: {output_path}")

if __name__ == "__main__":
    prompt_path = "prompts/income_statement_prompt.txt"
    prompt = load_prompt(prompt_path)
    print("📤 Sending prompt to Mistral...")
    result = run_mistral(prompt)
    print("🤖 Mistral's Response:\n")
    print(result)
    save_output(result)
