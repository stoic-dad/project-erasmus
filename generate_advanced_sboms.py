import json
import os
import random

# Ensure sboms directory exists
os.makedirs('sboms', exist_ok=True)

vendors = [
    'AcmeCorp', 'Globex', 'Initech', 'UmbrellaCorp', 'Hooli',
    'StarkIndustries', 'WayneEnterprises', 'WonkaIndustries', 'Cyberdyne',
    'TyrellCorp'
]

countries = ['USA', 'France', 'Germany', 'China', 'India', 'Brazil', 'UK', 'Japan']
severities = ['critical', 'high', 'medium']
levels = ['level 0', 'level 1', 'level 2', 'level 3']

for i in range(1, 51):  # Generate 50 SBOM files
    components = []
    num_components = random.randint(5, 15)

    for j in range(num_components):
        num_cves = random.randint(0, 5)
        cves = [
            {
                "id": f"CVE-2023-{random.randint(1000,9999)}",
                "severity": random.choice(severities)
            }
            for _ in range(num_cves)
        ]

        component = {
            "publisher": random.choice(vendors),
            "name": f"component-{j}",
            "version": f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}",
            "level": random.choice(levels),
            "cves": cves
        }
        components.append(component)

    sbom = {"components": components}

    file_path = f"sboms/sample{i}.json"
    with open(file_path, 'w') as f:
        json.dump(sbom, f, indent=2)

print("✅ Generated 50 advanced SBOMs in the sboms/ folder.")