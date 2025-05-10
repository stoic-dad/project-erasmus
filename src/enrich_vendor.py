import pandas as pd

def enrich_vendors(components_df, vendor_geo_file):
    # Load vendor geo data
    vendor_geo = pd.read_csv(vendor_geo_file)
    
    # Merge on supplier name
    enriched_df = components_df.merge(
        vendor_geo, 
        how='left', 
        left_on='supplier', 
        right_on='vendor'
    )
    
    # Fill missing geo info
    enriched_df['hq_country'].fillna('Unknown', inplace=True)
    enriched_df['geo_region'].fillna('Unknown', inplace=True)
    
    return enriched_df