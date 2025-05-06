import json
import sys
import plotly.graph_objects as go

def generate_sankey(filepath):
    # Load JSON file
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return
    except json.JSONDecodeError:
        print(f"❌ File is not valid JSON: {filepath}")
        return

    # Extract metadata
    company = data.get("company", "Company")
    year = data.get("year", "Year")
    sections = data.get("sections", {})

    if not sections:
        print("❌ No sections found in the JSON file. Expected a 'sections' object.")
        return

    labels = []
    sources = []
    targets = []
    values = []
    label_index = {}

    def get_index(label):
        if label not in label_index:
            label_index[label] = len(labels)
            labels.append(label)
        return label_index[label]

    # Loop through each section (e.g., Revenue, Expenses, Net Income)
    for category, items in sections.items():
        if isinstance(items, dict):
            for sub_label, value in items.items():
                src = get_index(sub_label)
                tgt = get_index(category)
                sources.append(src)
                targets.append(tgt)
                values.append(value)
        elif isinstance(items, (int, float)):
            # Handle top-level number like "Net Income": 14000000
            src = get_index("Total Revenue")
            tgt = get_index(category)
            sources.append(src)
            targets.append(tgt)
            values.append(items)

    # Create Sankey diagram
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            label=labels
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    ))

    fig.update_layout(
        title_text=f"{company} Income Flow ({year})",
        font_size=12
    )

    fig.show()

# Run with: python generate_sankey.py data/disney_2023.json
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_sankey.py <path_to_json>")
    else:
        json_path = sys.argv[1]
        generate_sankey(json_path)
