from . import views
from django.urls import path

urlpatterns = [
    
    path('', views.home, name="dashboard"),
    path('home/', views.bkash, name="bkash")
]
    
    
    
