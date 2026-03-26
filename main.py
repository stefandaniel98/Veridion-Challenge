import pandas as pd
import json
import os
# Import our helper functions
from utils import get_page_content, check_for_techs

def start_scanner():
    # My project data files 
    input_file = 'data.snappy.parquet'
    rules_file = 'tech_signatures.json'
    output_file = 'results.json'

    # Check if files are present in the folder
    if not os.path.exists(input_file):
        print(f"Error: I can't find {input_file} in this folder.")
        return
    if not os.path.exists(rules_file):
        print(f"Error: I can't find {rules_file} in this folder.")
        return
    
    print("--- Loading website list from Parquet ---")
    try:
        df = pd.read_parquet(input_file)
        # We only need the root domains for crawling
        domains = df['root_domain'].tolist()
    except Exception as e:
        print(f"Error reading the parquet file: {e}")
        return

    # Loading the technology signatures
    with open(rules_file, 'r') as f:
        config_data = json.load(f)
        all_rules = config_data.get('technologies', [])

    final_results = []
    
    # Process the domains
    print(f"Found {len(domains)} sites. Starting the crawl...")

    for site in domains:
        print(f"Searching on: {site}")
        
        # Step 1: Crawl the page
        data = get_page_content(site)

        if data:
            # Step 2: Detect technologies
            found_list = check_for_techs(data['html'], data['headers'], all_rules)
            final_results.append({
                "domain": site,
                "technologies": found_list,
                "status": "success"
            })
        else:
            final_results.append({
                "domain": site,
                "technologies": [],
                "status": "failed"
            })

    # Summary of my scanning process
    total_detected = sum(len(result['technologies']) for result in final_results)
    failed_domains = sum(1 for result in final_results if result['status'] == 'failed')
    
    # A simple printout of my results
    print("\n" + "="*35)
    print(f" Scan summary:")
    print(f" Total domains processed: {len(domains)}")
    print(f" Total technologies identified: {total_detected}")
    print(f" Total failed domains: {failed_domains}")
    print("="*35)

    # Saving everything to results.json
    print(f"Finished! Saving results to {output_file}")
    with open(output_file, 'w') as f:
        json.dump(final_results, f, indent=4)

if __name__ == "__main__":
    start_scanner()