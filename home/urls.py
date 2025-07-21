from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.home,name=''),
    path('traffic_accidents',views.traffic_accidents,name='traffic_accidents'),
    path('rainfall_data',views.rainfall_data,name='rainfall_data'),
]