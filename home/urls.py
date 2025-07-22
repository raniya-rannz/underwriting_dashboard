from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.home,name=''),
    path('traffic_accidents',views.traffic_accidents,name='traffic_accidents'),
    path('rainfall_data',views.rainfall_data,name='rainfall_data'),
    #####################REST API URLs########################
    path('api/v1/data/traffic/accidents/api', views.UnderWritingRiskGet.as_view({'get': 'list_traffic'}), name='traffic_accidents_api'),
    path('api/v1/data/rainfall/data/api', views.UnderWritingRiskGet.as_view({'get': 'list_rainfall'}), name='rainfall_data_api'),
]