from django.urls import path

from .views import *

urlpatterns = [
    path("", upload_data, name="upload_data"),
    path('filter/', filter_data, name='filter_data'),
    path('display_data/',display_data,name='display_data')
]