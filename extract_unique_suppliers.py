import sys
import os
sys.path.append('src')

from parse_sbom import extract_components

sbom_folder = 'sboms'
unique_suppliers = set()

for sbom_file in os.listdir(sbom_folder):
    if sbom_file.endswith('.json'):
        path = os.path.join(sbom_folder, sbom_file)
        components = extract_components(path)
        unique_suppliers.update(components['supplier'].unique())

with open('unique_suppliers.txt', 'w') as f:
    for supplier in sorted(unique_suppliers):
        f.write(f"{supplier}\n")

print("✅ Unique suppliers saved to unique_suppliers.txt")