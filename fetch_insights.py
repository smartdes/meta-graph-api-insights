import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")  # Uses your specific Page ID

def get_page_metrics():
    if not ACCESS_TOKEN or not PAGE_ID:
        print("Error: META_ACCESS_TOKEN or PAGE_ID missing from .env file.")
        return None

    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/insights"
    params = {
        'metric': 'page_impressions,page_post_engagements',
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching data: {response.json()}")
        return None
        
    return response.json()

def process_data(raw_data):
    if not raw_data or 'data' not in raw_data:
        print("No metrics data returned.")
        return
    
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
    df.to_csv("insights_summary.csv", index=False)
    print("Successfully exported insights to insights_summary.csv")

if __name__ == "__main__":
    data = get_page_metrics()
    if data:
        process_data(data)