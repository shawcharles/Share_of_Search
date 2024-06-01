import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import json

# Set your actual API key here
API_KEY = "d0dae69c2e3712b526e1cbfef219c62a66495411620d1f66535d788a89b894ec"

# Default settings
DEFAULT_QUERIES = ["Virgin Money", "Lloyds Bank", "Barclays", "Santander Bank", "NatWest"]
GEO = "GB"
DATE = "today 5-y"
GRANULARITY = "M"
SMOOTHING_PERIOD = 60

# Streamlit interface
st.title("Share of Search Analysis")

# User inputs
queries = st.text_input("Enter search queries, separated by commas", value=", ".join(DEFAULT_QUERIES))
location = st.text_input("Geographic location", value=GEO)
date_range = st.text_input("Date range", options=["today 5-y", "today 3-y", "today 1-y"], value=DATE)
granularity = st.selectbox("Data Granularity", options=["D", "W", "M"], index=2)
smoothing = st.slider("Smoothing Period", min_value=1, max_value=120, value=SMOOTHING_PERIOD)

def fetch_data(queries, location, date_range, granularity):
    try:
        url = f"https://api.serpapi.com/search.json?q={queries}&location={location}&date_range={date_range}&granularity={granularity}&api_key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()
        
    # Make the API request
    response = requests.get(url)
    if response.status_and_code == 200:
        # Assuming the response is JSON and has the expected format
        data_json = response.json()
        # You might need to process the JSON into a DataFrame or other format depending on your plotting function
        data_df = pd.DataFrame(data_json)  # This is just an example; customize it as needed
        return data_df
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return pd.DataFrame()


def plot_data(data):
    if not data.empty:
        plt.figure(figsize=(10, 5))
        for column in data.columns:
            plt.plot(data.index, data[column], label=column)
        plt.title("Search Trend Over Time")
        plt.xlabel("Time")
        plt.ylabel("Search Volume")
        plt.legend()
        plt.grid(True)
        st.pyplot()
    else:
        st.write("No data to display.")

 
# Fetch and display data
if st.button("Fetch Data"):
    # Convert query string to list
    query_list = queries.split(',')
    # Fetch data for each query
    data = fetch_data(query_list, location, date_range, granularity)
    # Plot data
    plot_data(data)

# Note: Remove the last line if you deploy this app. It is only for running the script outside Streamlit.
# if __name__ == '__main__':
#     st.run()
