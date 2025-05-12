import sys
sys.path.append('src')

import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from parse_sbom import extract_components, extract_cve_and_levels, extract_vulnerabilities
from enrich_vendor import enrich_vendors
from display import call_ollama

st.set_page_config(page_title="SBOM Enrichment Dashboard", layout="wide")
st.title("🔍 SBOM Enrichment Dashboard")

# --- MODEL SELECTOR ---
st.sidebar.title("🧠 Model Settings")
model_choice = st.sidebar.selectbox(
    "Choose Ollama model:",
    options=["qwen2.5-coder:7b", "gemma:2b", "openhermes:latest"],
    index=0
)

# --- SBOM SELECTION ---
sbom_files = [f for f in os.listdir('sboms') if f.endswith('.json')]
sbom_choice = st.selectbox("Select an SBOM file:", sbom_files)

if sbom_choice:
    sbom_path = os.path.join("sboms", sbom_choice)
    components = extract_components(sbom_path)
    enriched = enrich_vendors(components, 'data/vendor_geo.csv')

    if not enriched.empty:
        st.subheader("📊 Enriched Vendor Data")
        st.dataframe(enriched)

        # --- CVE + LEVEL CHARTS ---
        severity_counts, level_counts = extract_cve_and_levels(sbom_path)

        st.subheader("🛡️ CVE Severity Counts")
        cve_df = pd.DataFrame(list(severity_counts.items()), columns=['Severity', 'Count'])
        st.bar_chart(cve_df.set_index('Severity'))

        st.subheader("⚙️ Component Levels")
        level_df = pd.DataFrame(list(level_counts.items()), columns=['Level', 'Count'])

        # Convert 'Count' to numeric, coercing errors to NaN
        level_df['Count'] = pd.to_numeric(level_df['Count'], errors='coerce')

        # Drop rows with NaN or non-positive 'Count' values
        level_df = level_df.dropna(subset=['Count'])
        level_df = level_df[level_df['Count'] > 0]

        if not level_df.empty:
            fig, ax = plt.subplots()
            ax.pie(level_df['Count'], labels=level_df['Level'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
        else:
            st.warning("⚠️ Component level data is missing or malformed.")

        # --- VULNERABILITY TABLE (OPTIONAL) ---
        vuln_file = f'sboms_vulns/{sbom_choice.replace(".json", "-vulns.json")}'
        if os.path.exists(vuln_file):
            vulns_df = extract_vulnerabilities(vuln_file)
            if not vulns_df.empty:
                st.subheader("🛡️ Vulnerability Details")
                st.dataframe(vulns_df[['id', 'severity', 'affects', 'description']])

                severity_summary = vulns_df['severity'].value_counts()
                st.subheader("⚙️ Vulnerability Severity Summary")
                st.bar_chart(severity_summary)

        # --- OLLAMA SUMMARIZATION ---
        summary_input = enriched.head(20).to_string(index=False)
        prompt = (
            f"Summarize this enriched SBOM vendor data and highlight geographic or supply chain risks:\n\n{summary_input}"
        )

        if st.button("💬 Run Ollama Summary"):
            st.info(f"⏳ Calling Ollama model: {model_choice}...")
            summary = call_ollama(prompt, model=model_choice)
            st.subheader("💬 Ollama Summary")
            st.write(summary)

        # --- FOLLOW-UP QUESTION ---
        user_question = st.text_input("Ask a follow-up question:")
        if st.button("💬 Ask"):
            followup_prompt = (
                f"Based on this enriched SBOM data, answer the following question:\n"
                f"{user_question}\n\n"
                f"Data:\n{summary_input}"
            )
            st.info(f"⏳ Asking {model_choice}...")
            answer = call_ollama(followup_prompt, model=model_choice)
            st.subheader("💬 Ollama Answer")
            st.write(answer)
    else:
        st.warning("⚠️ No enrichment data found. Check vendor_geo.csv or SBOM format.")