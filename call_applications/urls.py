from django.urls import path, include
from .views import *

urlpatterns = [
    path('', open_application, name="open_applcations"),
    path('<pk>/', application_detail, name="open_application_detail")
]
