from django.shortcuts import render
from . import functions
import requests
from django.core.paginator import Paginator
from django.http import Http404
import pandas as pd
import math
from rest_framework.viewsets import GenericViewSet
from generics import exceptions
from rest_framework.pagination import LimitOffsetPagination
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, OpenApiParameter
from . import serializers
from rest_framework.response import Response 
from drf_spectacular.types import OpenApiTypes
from . import models
from rest_framework.permissions import AllowAny

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


##########################
# REST API Views #
###########################

class UnderWritingRiskGet(GenericViewSet):
    authentication_classes = []  # Disable authentication
    permission_classes = []      # Allow unrestricted access
    pagination_class = LimitOffsetPagination

    @extend_schema(
    tags=[' Traffic accidents'],
        summary='to list all traffic accidents by pagination. no other filters',
        description="""
        to list all recors by pagination. no other filters
        """,
        parameters=[

        OpenApiParameter(name='limit', required=True, type=int,location=OpenApiParameter.QUERY),
        OpenApiParameter(name='offset', required=True, type=int,location=OpenApiParameter.QUERY),
        OpenApiParameter(name="type", description="Filter accidents by type", required=False, type=OpenApiTypes.STR),
        OpenApiParameter(name="year", description="Filter accidents by year", required=False, type=OpenApiTypes.STR),
        ],
    responses={
        200:dict,
        400:dict,
    }
    )
    def list_traffic(self,request):
        limit=int(request.query_params.get('limit'))
        offset=int(request.query_params.get('offset'))
        year = request.query_params.get('year', None)
        result_of_the_accident = request.query_params.get('type', None)


        data=models.TrafficAccident.objects.all()

        if year:
            data = data.filter(year=year)
        if result_of_the_accident:
            data = data.filter(result_of_the_accident__icontains=result_of_the_accident)
        
        result_page=self.paginate_queryset(data)
        serializer=serializers.TrafficAccidentSerializer(result_page,many=True)
        result_data=self.get_paginated_response(serializer.data) 

        return Response(result_data.data)

    @extend_schema(
    tags=[' Rainfall Records'],
        summary='to list all rainfall recors by pagination. no other filters',
        description="""
        to list all recors by pagination. no other filters
        """,
        parameters=[

        OpenApiParameter(name='limit', required=True, type=int,location=OpenApiParameter.QUERY),
        OpenApiParameter(name='offset', required=True, type=int,location=OpenApiParameter.QUERY),
        OpenApiParameter(name="station", description="Filter rainfall by station", required=False, type=OpenApiTypes.STR),
        OpenApiParameter(name="year", description="Filter rainfall by year", required=False, type=OpenApiTypes.STR),
        ],
    responses={
        200:dict,
        400:dict,
    }
    )
    def list_rainfall(self,request):
        limit=int(request.query_params.get('limit'))
        offset=int(request.query_params.get('offset'))
        year = request.query_params.get('year', None)
        station = request.query_params.get('station', None)


        data=models.RainfallRecord.objects.all()

        if year:
            data = data.filter(year=year)
        if station:
            data = data.filter(station__icontains=station)
        
        result_page=self.paginate_queryset(data)
        serializer=serializers.RainfallRecordSerializer(result_page,many=True)
        result_data=self.get_paginated_response(serializer.data) 

        return Response(result_data.data)
