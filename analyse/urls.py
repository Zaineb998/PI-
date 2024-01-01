from django.urls import path

from .views import *

urlpatterns = [
    path("upload_data/", upload_data, name="upload_data"),
    path('',display_titles, name='display_titles'),
    path('<str:titre>/',display_chart, name='chart_page'),
    path('delete/delete',delete_all_data,name='delete_all_data')
]