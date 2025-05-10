import sys
import os
sys.path.append('src')

import streamlit as st
import pandas as pd
from parse_sbom import extract_components, extract_cve_and_levels, extract_vulnerabilities
from enrich_vendor import enrich_vendors
from display import call_ollama

st.set_page_config(page_title="SBOM Enrichment Dashboard", layout="wide")
st.title("🔍 SBOM Enrichment Dashboard")

# List available SBOM files
sbom_files = [f for f in os.listdir('sboms') if f.endswith('.json')]
sbom_choice = st.selectbox("Select an SBOM file:", sbom_files)

if sbom_choice:
    sbom_path = os.path.join('sboms', sbom_choice)
    vuln_path = os.path.join('sboms_vulns', sbom_choice.replace('.json', '-vulns.json'))

    # Load components + enrich vendors
    components_df = extract_components(sbom_path)
    enriched_df = enrich_vendors(components_df, 'data/vendor_geo.csv')

    if enriched_df.empty:
        st.warning("No enriched vendor data available.")
    else:
        st.subheader("📦 Enriched Components")
        st.dataframe(enriched_df)

        # Limit Ollama input to first 20 rows + key columns
        summary_input_short = enriched_df[['name', 'supplier', 'license']].head(20).to_string(index=False)
        prompt = (
            f"Summarize this enriched SBOM vendor data (sample of first 20 rows) and highlight interesting "
            f"geographic or supply chain risks:\n\n{summary_input_short}"
        )

        if st.button("💬 Run Ollama Summary"):
            summary = call_ollama(prompt, model='llama3.2')
            st.subheader("💬 Ollama Summary")
            st.write(summary)

        user_question = st.text_input("Ask a follow-up question:")
        if st.button("💬 Ask"):
            followup_prompt = (
                f"Based on this sample of enriched SBOM data (first 20 rows), answer the following question:\n"
                f"{user_question}\n\n"
                f"Data sample:\n{summary_input_short}"
            )
            answer = call_ollama(followup_prompt, model='llama3.2')
            st.subheader("💬 Ollama Answer")
            st.write(answer)

    # Dummy or real CVE + level data
    severity_counts, level_counts = extract_cve_and_levels(sbom_path)
    if any(severity_counts.values()):
        st.subheader("🛡️ CVE Severity Counts")
        st.bar_chart(pd.Series(severity_counts))
        st.subheader("⚙️ Component Levels")
        st.bar_chart(pd.Series(level_counts))

    # Load vulnerabilities if file exists
    if os.path.exists(vuln_path):
        vuln_df = extract_vulnerabilities(vuln_path)
        if not vuln_df.empty:
            st.subheader("🔎 Vulnerabilities")
            st.dataframe(vuln_df)
        else:
            st.info("No vulnerabilities found.")
    else:
        st.info("No vulnerabilities file found for this SBOM.")