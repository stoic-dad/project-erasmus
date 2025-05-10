import pandas as pd

# Read suppliers from text file
with open('unique_suppliers.txt', 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# Filter out system file paths
filtered_lines = [line for line in lines if not line.startswith(('/etc', '/usr', '/var'))]

# Build DataFrame
suppliers = pd.DataFrame(filtered_lines, columns=['vendor'])

def map_country(vendor):
    name = str(vendor).lower()
    if 'gmbh' in name:
        return 'Germany', 'Europe'
    elif 'inc' in name or 'llc' in name:
        return 'USA', 'North America'
    elif 'sas' in name:
        return 'France', 'Europe'
    elif '.cn' in name:
        return 'China', 'Asia'
    elif '.co.jp' in name:
        return 'Japan', 'Asia'
    else:
        return 'Unknown', 'Unknown'

# Apply mapping
suppliers[['hq_country', 'geo_region']] = suppliers['vendor'].apply(lambda x: pd.Series(map_country(x)))

# Save to CSV
suppliers.to_csv('vendor_geo.csv', index=False)

print(f"✅ vendor_geo.csv created with {len(suppliers)} rows (system files excluded!)")