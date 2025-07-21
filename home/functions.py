import requests
import pandas as pd
from collections import OrderedDict
from . import models

def traffic_accidents_db_save():
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

    save_traffic_db = [
    models.TrafficAccident.objects.create(
        year=int(row['year']),
        result_of_the_accident=row['result_of_the_accident'],
        number_of_people=int(row['number_of_people']),
        result_of_the_accident_ar=row['result_of_the_accident_ar']
    )
    for row in df.to_dict(orient='records')
    if not models.TrafficAccident.objects.filter(
        year=int(row['year']),
        result_of_the_accident=row['result_of_the_accident']
    ).exists()
    ]   
    return df


def rainfall_data_db_save():
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

    save_rainfall_db = [
        models.RainfallRecord.objects.create(
            station=row['station'],
            year=int(row['year']),
            rainfall_mm=float(row['rainfall_mm'])
        )
        for _, row in grouped_df.iterrows()
        if not models.RainfallRecord.objects.filter(station=row['station'], year=int(row['year'])).exists()
    ]
    return grouped_df


def traffic_accidents_get():
    data=models.TrafficAccident.objects.all().values(
        'year', 'result_of_the_accident', 'number_of_people', 'result_of_the_accident_ar'
    )
    df = pd.DataFrame(list(data))
    return df

def rainfall_data_get():
    data = models.RainfallRecord.objects.all().values(
        'station', 'year', 'rainfall_mm'
    )
    df = pd.DataFrame(list(data))
    if not df.empty:
        df['rainfall_mm'] = df['rainfall_mm'].astype(float)
    return df
