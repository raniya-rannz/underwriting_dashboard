import requests
import pandas as pd
from collections import OrderedDict

def traffic_accidents_get():
    url = "https://www.data.gov.qa/api/explore/v2.1/catalog/datasets/number-of-deaths-and-injuries-from-traffic-accidents/records"
    limit = 100
    offset = 0
    all_records = []

    while True:
        params = {
            "limit": limit,
            "offset": offset
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        records = data.get('results', [])
        if not records:
            break  # no more records

        all_records.extend(records)
        if len(records) < limit:
            # Last batch (fewer than limit)
            break
        
        offset += limit  # next batch offset

    # Convert to DataFrame
    df = pd.DataFrame(all_records)

    # Convert year to numeric and drop invalid
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df.dropna(subset=['year'])

    # Sort by year descending
    df = df.sort_values(by='year', ascending=False).reset_index(drop=True)

    return df


def rainfall_data_get():
    url = "https://www.data.gov.qa/api/explore/v2.1/catalog/datasets/rainfall-average-mm-at-selected-monitoring-stations-in-qatar/records"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    records = data.get('results', [])

    df = pd.DataFrame(records)
    df_long = df.melt(id_vars=['station'], var_name='year', value_name='rainfall_mm')
    df_long['year'] = pd.to_numeric(df_long['year'], errors='coerce')
    df_long['rainfall_mm'] = pd.to_numeric(df_long['rainfall_mm'], errors='coerce')
    df_long = df_long.dropna(subset=['year', 'rainfall_mm'])
    grouped_df = df_long.groupby(['station', 'year'], as_index=False)['rainfall_mm'].mean()
    grouped_df = grouped_df.sort_values(by=['station', 'year'], ascending=[True, False])
    return grouped_df

def real_estate_get(limit=1000):
    API_URL = "https://www.data.gov.qa/api/explore/v2.1/catalog/datasets/weekly-real-estate-newsletter/records"
    all_results = []
    offset = 0
    limit = 100

    while True:
        response = requests.get(API_URL, params={"limit": limit, "offset": offset})
        if response.status_code != 200:
            print(f"Error fetching at offset {offset}: {response.status_code}")
            break

        batch = response.json().get("results", [])
        if not batch:
            break  # No more data

        all_results.extend(batch)
        offset += limit

    df = pd.DataFrame(all_results)

    if 'municipality_name' not in df.columns:
        print("Field 'municipality_name' missing.")
        return {}

    df = df.dropna(subset=['municipality_name'])

    grouped = df.groupby("municipality_name")
    result = {muni: group.to_dict(orient="records") for muni, group in grouped}
    return result