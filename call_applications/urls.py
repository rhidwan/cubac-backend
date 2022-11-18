from django.urls import path, include
from .views import *

urlpatterns = [
    path('', open_application, name="open_applications"),
    path('edit/<pk>/', edit_open_application_detail, name="edit_open_application_detail"),
    path('view/<slug>/', open_application_detail, name="open_application_detail"),
    path('api/', api_open_application, name="api_open_applcations"),
    path('api/<pk>/', api_application_detail, name="api_open_application_detail"),
]
