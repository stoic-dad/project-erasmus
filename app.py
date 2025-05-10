import sys
sys.path.append('src')

import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from parse_sbom import extract_vendors, extract_cve_and_levels
from enrich_vendor import enrich_vendors
from display import call_ollama

# List SBOMs
sbom_files = [f for f in os.listdir('sboms') if f.endswith('.json') or f.endswith('.spdx')]

st.set_page_config(page_title="SBOM Enrichment Dashboard", layout="wide")
st.title("🔍 SBOM Enrichment Dashboard")

sbom_choice = st.selectbox("Select an SBOM file:", sbom_files)

if sbom_choice:
    vendors = extract_vendors(f'sboms/{sbom_choice}')
    enriched = enrich_vendors(vendors, 'data/vendor_geo.csv')

    if not enriched.empty:
        st.subheader("📊 Enriched Vendor Data")
        st.dataframe(enriched)

        # ⏩ NEW: get CVE + level data
        severity_counts, level_counts = extract_cve_and_levels(f'sboms/{sbom_choice}')

        # ⏩ NEW: CVE bar chart
        st.subheader("🛡️ CVE Severity Counts")
        cve_df = pd.DataFrame(list(severity_counts.items()), columns=['Severity', 'Count'])
        st.bar_chart(cve_df.set_index('Severity'))

        # ⏩ NEW: Component level pie chart
        st.subheader("⚙️ Component Levels")
        level_df = pd.DataFrame(list(level_counts.items()), columns=['Level', 'Count'])
        fig, ax = plt.subplots()
        ax.pie(level_df['Count'], labels=level_df['Level'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

        summary_input = enriched.to_string(index=False)
        prompt = (
            f"Summarize this enriched SBOM vendor data and highlight interesting "
            f"geographic or supply chain risks:\n\n{summary_input}"
        )

        if st.button("💬 Run Ollama Summary"):
            summary = call_ollama(prompt, model='llama3.2')
            st.subheader("💬 Ollama Summary")
            st.write(summary)

        user_question = st.text_input("Ask a follow-up question:")
        if st.button("💬 Ask"):
            followup_prompt = (
                f"Based on this enriched SBOM data, answer the following question:\n"
                f"{user_question}\n\n"
                f"Data:\n{summary_input}"
            )
            answer = call_ollama(followup_prompt, model='llama3.2')
            st.subheader("💬 Ollama Answer")
            st.write(answer)
    else:
        st.warning("⚠️ No enrichment data found. Check vendor_geo.csv.")