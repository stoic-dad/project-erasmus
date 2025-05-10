import pandas as pd

def enrich_vendors(vendors, csv_file):
    lookup = pd.read_csv(csv_file)
    enriched = lookup[lookup['vendor'].isin(vendors)]
    return enriched