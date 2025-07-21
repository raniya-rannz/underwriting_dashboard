from django.shortcuts import render
from . import functions
import requests
from django.core.paginator import Paginator
from django.http import Http404
import pandas as pd
import math
# Create your views here.

def login(request):
    return render(request,"login.html")

def home(request):
    return render(request,"home.html")

def traffic_accidents(request):
    df = functions.traffic_accidents_get()
    if df is not None and not df.empty:
        # Convert DataFrame to dict records for template context
        accidents = df.to_dict(orient='records')
        context = {'accidents': accidents}
    else:
        context = {'error': 'Failed to retrieve data from the API or no data found.'}

    return render(request, "traffic_accidents.html", context)

def rainfall_data(request):
    df = functions.rainfall_data_get()

    if df is not None and not df.empty:
        rainfall = df.to_dict(orient='records')
        unique_stations = sorted(df['station'].dropna().unique())
        unique_years = sorted(df['year'].dropna().unique())

        # Create nested dict: rainfall_lookup[year][station] = rainfall_mm
        rainfall_lookup = {}
        for row in rainfall:
            year = int(row['year'])
            station = row['station']
            rainfall_mm = round(row['rainfall_mm'], 2)

            if year not in rainfall_lookup:
                rainfall_lookup[year] = {}
            rainfall_lookup[year][station] = rainfall_mm

        context = {
            'stations': unique_stations,
            'years': unique_years,
            'rainfall_lookup': rainfall_lookup,
        }
    else:
        context = {
            'error': 'Failed to retrieve data from the API or no data found.'
        }

    return render(request, "rainfall_data.html", context)


def realestate_data(request):
    selected_muni = request.GET.get('municipality')
    page = int(request.GET.get('page', 1))
    municipalities_per_page = 3

    # Step 1: Get all municipalities
    muni_url = "https://www.data.gov.qa/api/explore/v2.1/catalog/datasets/weekly-real-estate-newsletter/records"
    muni_resp = requests.get(muni_url, params={"group_by": "municipality_name", "limit": 100})

    if muni_resp.status_code != 200:
        return render(request, "real_estate_newsletter.html", {"error": "Failed to fetch municipality list"})

    muni_list = sorted(set(item["municipality_name"] for item in muni_resp.json().get("results", [])))
    grouped_data = []

    if selected_muni:
        # Only fetch and show selected municipality
        resp = requests.get(muni_url, params={"refine": f"municipality_name:{selected_muni}", "limit": 100})
        if resp.status_code == 200:
            df = pd.DataFrame(resp.json().get("results", []))
            grouped_data.append({
                "municipality_name": selected_muni,
                "records": df.to_dict(orient="records")
            })
        total_pages = 1
        page_range = [1]
    else:
        # Paginated fetch of all municipalities
        total_pages = math.ceil(len(muni_list) / municipalities_per_page)
        start_idx = (page - 1) * municipalities_per_page
        end_idx = start_idx + municipalities_per_page
        selected_munis = muni_list[start_idx:end_idx]

        for muni in selected_munis:
            resp = requests.get(muni_url, params={"refine": f"municipality_name:{muni}", "limit": 100})
            if resp.status_code == 200:
                df = pd.DataFrame(resp.json().get("results", []))
                grouped_data.append({
                    "municipality_name": muni,
                    "records": df.to_dict(orient="records")
                })

        # Pagination range
        start_page = max(page - 1, 1)
        end_page = min(start_page + 2, total_pages)
        start_page = max(end_page - 2, 1)
        page_range = range(start_page, end_page + 1)

    return render(request, "real_estate_newsletter.html", {
        "groups": grouped_data,
        "municipality_list": muni_list,
        "selected_municipality": selected_muni,
        "page": page,
        "total_pages": total_pages,
        "page_range": page_range,
    })