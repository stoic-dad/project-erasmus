import pandas as pd
import json

def extract_components(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        if not content.strip():
            return pd.DataFrame()
        sbom = json.loads(content)

    components = []
    for comp in sbom.get('components', []):
        supplier_field = comp.get('supplier')
        if isinstance(supplier_field, dict):
            supplier = supplier_field.get('name')
        elif isinstance(supplier_field, str):
            supplier = supplier_field
        else:
            supplier = None

        publisher_field = comp.get('publisher')
        if isinstance(publisher_field, dict):
            publisher = publisher_field.get('name')
        elif isinstance(publisher_field, str):
            publisher = publisher_field
        else:
            publisher = None

        supplier = supplier or publisher or comp.get('name') or 'Unknown'

        components.append({
            'name': comp.get('name'),
            'version': comp.get('version'),
            'type': comp.get('type'),
            'supplier': supplier,
            'license': comp.get('licenses', [{}])[0].get('license', {}).get('id', 'Unknown'),
            'hash': comp.get('hashes', [{}])[0].get('content', 'N/A'),
            'level': comp.get('properties', [{}])[0].get('name', 'level-0')
        })
    return pd.DataFrame(components)

def extract_cve_and_levels(file_path):
    return {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}, {'Level 0': 0, 'Level 1': 0}

def extract_vulnerabilities(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        if not content.strip():
            return pd.DataFrame()
        sbom_vulns = json.loads(content)

    vulns = []
    for vuln in sbom_vulns.get('vulnerabilities', []):
        vulns.append({
            'id': vuln.get('id'),
            'source': vuln.get('source', {}).get('name', 'Unknown'),
            'severity': vuln.get('ratings', [{}])[0].get('severity', 'Unknown'),
            'description': vuln.get('description', 'No description'),
            'affects': vuln.get('affects', [{}])[0].get('ref', 'Unknown'),
        })
    return pd.DataFrame(vulns)