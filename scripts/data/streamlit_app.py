import streamlit as st
import json
import plotly.graph_objects as go

# Load JSON file
with open("data/parsed/disney_d3_ready_2024.json") as f:
    data = json.load(f)

# Extract nodes and links
nodes = data["nodes"]
links = data["links"]

# Prepare node labels
labels = [node["name"] for node in nodes]

# Prepare link data
sources = [link["source"] for link in links]
targets = [link["target"] for link in links]
values = [link["value"] for link in links]

# Plotly Sankey chart
fig = go.Figure(data=[
    go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    )
])

fig.update_layout(title_text=f"{data['company']} Income Flow ({data['year']})", font_size=12)

# Streamlit app
st.title("Financial Storytelling: Sankey Diagram")
st.plotly_chart(fig)

st.markdown("---")
st.markdown(f"**Company:** {data['company']}")
st.markdown(f"**Year:** {data['year']}")
