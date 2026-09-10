import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_page_metrics(access_token=None, page_id=None, metrics=['page_impressions', 'page_post_engagements']):
    """Fetches insights data from Meta Graph API using provided credentials or .env fallback."""
    token = access_token or os.getenv("META_ACCESS_TOKEN")
    p_id = page_id or os.getenv("PAGE_ID")

    if not token or not p_id:
        print("Error: META_ACCESS_TOKEN or PAGE_ID is missing.")
        return None

    url = f"https://graph.facebook.com/v19.0/{p_id}/insights"
    params = {
        'metric': ','.join(metrics),
        'access_token': token
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching data: {response.json()}")
        return None
        
    return response.json()

def process_data(raw_data, filename="insights_summary.csv"):
    """Processes raw JSON response into a DataFrame and exports to CSV."""
    if not raw_data or 'data' not in raw_data:
        print("No metrics data returned.")
        return None
    
    metrics = []
    for item in raw_data['data']:
        name = item['name']
        values = item['values']
        for val in values:
            metrics.append({
                'metric': name,
                'end_time': val['end_time'],
                'value': val['value']
            })
            
    df = pd.DataFrame(metrics)
    df.to_csv(filename, index=False)
    print(f"Successfully exported insights to {filename}")
    return df

if __name__ == "__main__":
    data = get_page_metrics()
    if data:
        process_data(data)