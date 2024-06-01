import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Set your actual API key here
API_KEY = "bf3976c03caab6ea9b6c9627549552adf16e334d124a267405cc120cba926043"

def fetch_related_queries(search_term):
    # API parameters
    params = {
        'engine': 'google_trends',
        'q': search_term,
        'data_type': 'RELATED_QUERIES',
        'api_key': API_KEY  # Corrected variable name here
    }
    url = 'https://serpapi.com/search.json'
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        related_queries = data.get('related_queries', {})
        return related_queries
    else:
        st.error("Failed to fetch related queries: {} {}".format(response.status_code, response.text))
        return None

def save_queries(queries):
    keys = ['query', 'value']
    results = []
    for query in queries:
        row = {key: query.get(key, '') for key in keys}
        results.append(row)
    return results

def plot_queries(queries, title):
    df = pd.DataFrame(queries)
    df['value'] = pd.to_numeric(df['value'].str.strip('%+'))
    df = df.sort_values('value', ascending=True)
    plt.figure(figsize=(10, 8))
    plt.barh(df['query'], df['value'])
    plt.xlabel('Change in Interest')
    plt.title(title)
    plt.gca().invert_yaxis()
    st.pyplot(plt)

st.title("Related Queries Tracker")

search_term = st.text_input("Enter a search term", "Virgin Money")
if st.button("Fetch Related Queries"):
    related_queries = fetch_related_queries(search_term)
    if related_queries:  # Corrected the syntax here
        rising_queries = save_queries(related_results.get('rising', []))
        top_queries = save_queries(related_results.get('top', []))

        st.subheader('Rising Queries')
        st.write(pd.DataFrame(rising_queries))
        plot_queries(rising_queries, 'Rising Queries for ' + search_term)

        st.subheader('Top Queries')
        st.write(pd.DataFrame(top_queries))
        plot_queries(top_queries, 'Top Queries for ' + search_term)
