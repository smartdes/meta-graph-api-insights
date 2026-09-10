import os
import requests
import pandas as pd
import streamlit as st
import datetime
from dotenv import load_dotenv

# Page Configuration
st.set_page_config(
    page_title="Meta Graph API Insights",
    page_icon="📊",
    layout="wide"
)

# Load environment variables
load_dotenv()

# ---------------------------------------------------------
# SIDEBAR INPUT CONTROLS & AUTHENTICATION
# ---------------------------------------------------------
st.sidebar.title("🔑 Authentication & Setup")

default_token = os.getenv("META_ACCESS_TOKEN", "")
default_page_id = os.getenv("PAGE_ID", "")

access_token = st.sidebar.text_input(
    "Meta Access Token:", 
    value=default_token, 
    type="password"
)

page_id = st.sidebar.text_input(
    "Page ID / Project ID:", 
    value=default_page_id
)

st.sidebar.markdown("---")
st.sidebar.title("⚙️ Dashboard Parameters")

available_metrics = ['page_impressions', 'page_post_engagements']
selected_metrics = st.sidebar.multiselect(
    "Select Metrics to Query:",
    options=available_metrics,
    default=available_metrics
)

today = datetime.date.today()
default_start = today - datetime.timedelta(days=28)
date_range = st.sidebar.date_input(
    "Select Date Range:",
    value=(default_start, today)
)

min_threshold = st.sidebar.slider(
    "Highlight metric values above:",
    min_value=0,
    max_value=1000,
    value=10,
    step=5
)

fetch_button = st.sidebar.button("🚀 Fetch Data from API", use_container_width=True)

# ---------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------
def fetch_meta_insights(token, p_id, metrics):
    """Fetches selected insights metrics from Meta Graph API."""
    if not token or not p_id:
        st.error("Missing credentials! Please enter your Meta Access Token and Page ID.")
        return None

    url = f"https://graph.facebook.com/v19.0/{p_id}/insights"
    params = {
        'metric': ','.join(metrics),
        'access_token': token
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            err_msg = response.json().get('error', {}).get('message', 'Unknown error')
            st.error(f"API Error ({response.status_code}): {err_msg}")
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
                'Date': pd.to_datetime(val['end_time'][:10]),
                'Value': val['value']
            })
            
    return pd.DataFrame(metrics)

# ---------------------------------------------------------
# MAIN DASHBOARD OUTPUT DISPLAY
# ---------------------------------------------------------
st.title("📊 Interactive Meta Insights Analytics Dashboard")
st.markdown("Automated metrics extraction, security controls, and visual analytics pipeline for Facebook Pages.")

if fetch_button:
    if not selected_metrics:
        st.warning("Please select at least one metric from the sidebar.")
    else:
        with st.spinner("Connecting to Meta Graph API..."):
            raw_json = fetch_meta_insights(access_token, page_id, selected_metrics)
            if raw_json:
                st.session_state['df'] = process_data(raw_json)

if 'df' in st.session_state and not st.session_state['df'].empty:
    df = st.session_state['df']

    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
    else:
        df_filtered = df

    st.subheader("📌 Key Indicators Summary")
    cols = st.columns(len(selected_metrics))
    for idx, metric in enumerate(selected_metrics):
        metric_sum = df_filtered[df_filtered['Metric'] == metric]['Value'].sum()
        cols[idx].metric(label=f"Total {metric}", value=f"{metric_sum:,}")

    st.markdown("---")

    st.subheader("📈 Metric Trends Over Time")
    active_chart_metric = st.selectbox("Display Chart For Metric:", selected_metrics)
    chart_data = df_filtered[df_filtered['Metric'] == active_chart_metric]
    
    if not chart_data.empty:
        st.line_chart(chart_data.set_index('Date')['Value'])
    else:
        st.info("No data available for the selected date range.")

    st.markdown("---")

    st.subheader("📋 Filtered Data Table")
    threshold_df = df_filtered[df_filtered['Value'] >= min_threshold]
    st.dataframe(threshold_df, use_container_width=True)

    csv_data = threshold_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Output CSV",
        data=csv_data,
        file_name="filtered_insights_output.csv",
        mime="text/csv"
    )
else:
    st.info("Enter your credentials and parameters in the sidebar, then click **🚀 Fetch Data from API** to load the analytics dashboard.")