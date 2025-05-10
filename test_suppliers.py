import sys
sys.path.append('src')

from parse_sbom import extract_components

sbom_file = 'sboms/node-latest.json'
components = extract_components(sbom_file)

print("Unique suppliers in", sbom_file)
print(components['supplier'].unique())