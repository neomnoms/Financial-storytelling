# scripts/test_prompt_loader.py

def load_prompt(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    prompt_path = "prompts/income_statement_prompt.txt"
    prompt_text = load_prompt(prompt_path)
    print("📝 Loaded Prompt:\n")
    print(prompt_text)
