import json
import pandas as pd

def extract_vendors(sbom_file):
    with open(sbom_file) as f:
        sbom = json.load(f)
    return [comp['publisher'] for comp in sbom.get('components', []) if 'publisher' in comp]

def extract_cve_and_levels(sbom_file):
    with open(sbom_file) as f:
        sbom = json.load(f)

    severity_counts = {'critical': 0, 'high': 0, 'medium': 0}
    level_counts = {'level 0': 0, 'level 1': 0, 'level 2': 0, 'level 3': 0}

    for comp in sbom.get('components', []):
        for cve in comp.get('cves', []):
            severity = cve.get('severity')
            if severity in severity_counts:
                severity_counts[severity] += 1

        level = comp.get('level')
        if level in level_counts:
            level_counts[level] += 1

    return severity_counts, level_counts