from django.shortcuts import render
from . import functions
import requests
from django.core.paginator import Paginator
from django.http import Http404
import pandas as pd
import math
# Create your views here.


def home(request):
    return render(request,"home.html")

def traffic_accidents(request):
    df = functions.traffic_accidents_get()

    accidents = df.to_dict(orient='records')
    context = {'accidents': accidents}


    return render(request, "traffic_accidents.html", context)

def rainfall_data(request):
    df = functions.rainfall_data_get()

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

    return render(request, "rainfall_data.html", context)

