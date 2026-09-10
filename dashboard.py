import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Page Configuration
st.set_page_config(
    page_title="Meta Graph API Insights",
    page_icon="📊",
    layout="wide"
)

# Load environment variables
load_dotenv()
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

def fetch_meta_insights():
    """Fetches insights data from Meta Graph API."""
    if not ACCESS_TOKEN or not PAGE_ID:
        st.error("Missing credentials! Ensure META_ACCESS_TOKEN and PAGE_ID are set in your .env file.")
        return None

    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/insights"
    params = {
        'metric': 'page_impressions,page_post_engagements',
        'access_token': ACCESS_TOKEN
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error ({response.status_code}): {response.json().get('error', {}).get('message', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def process_data(raw_data):
    """Processes raw API JSON response into a clean Pandas DataFrame."""
    if not raw_data or 'data' not in raw_data:
        return pd.DataFrame()
    
    metrics = []
    for item in raw_data['data']:
        metric_name = item['name']
        for val in item['values']:
            metrics.append({
                'Metric': metric_name,
                'Date': val['end_time'][:10],
                'Value': val['value']
            })
            
    return pd.DataFrame(metrics)

# Sidebar Controls
st.sidebar.title("⚙️ Dashboard Controls")
st.sidebar.markdown("Fetch and visualize Meta Page insights in real-time.")
refresh_button = st.sidebar.button("🔄 Refresh Data from Meta API")

# Main Interface
st.title("📊 Meta Graph API Insights Dashboard")
st.markdown("Automated metrics extraction and visual analytics pipeline for Facebook Page engagement.")

# Data Fetching Logic
if refresh_button or 'insights_df' not in st.session_state:
    with st.spinner("Querying Meta Graph API..."):
        raw_json = fetch_meta_insights()
        if raw_json:
            st.session_state['insights_df'] = process_data(raw_json)

# Display Dashboard Content
if 'insights_df' in st.session_state and not st.session_state['insights_df'].empty:
    df = st.session_state['insights_df']

    # Metric KPI Highlights
    st.subheader("Key Metrics Summary")
    col1, col2 = st.columns(2)
    
    impressions_total = df[df['Metric'] == 'page_impressions']['Value'].sum()
    engagements_total = df[df['Metric'] == 'page_post_engagements']['Value'].sum()

    col1.metric("Total Page Impressions", f"{impressions_total:,}")
    col2.metric("Total Post Engagements", f"{engagements_total:,}")

    st.markdown("---")

    # Data Visualization
    st.subheader("📈 Metric Trends Over Time")
    selected_metric = st.selectbox("Select Metric to View:", df['Metric'].unique())
    filtered_df = df[df['Metric'] == selected_metric]

    st.line_chart(filtered_df.set_index('Date')['Value'])

    st.markdown("---")

    # Raw Data Table & Download Options
    st.subheader("📋 Raw Insights Data")
    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Summary as CSV",
        data=csv_data,
        file_name="meta_insights_summary.csv",
        mime="text/csv"
    )
else:
    st.info("Click **Refresh Data from Meta API** in the sidebar to fetch initial metrics.")