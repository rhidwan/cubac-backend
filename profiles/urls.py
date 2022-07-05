from re import M
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('basic_info/create/', create_basic_info, name="create_basic_info"),
    path('', user_detail, name="user_detail"),
    path('basic_info/', basic_info_detail, name="basic_info_detail"),
    path('test_score/', test_score, name="test_score"),
    path('test_score/<pk>/', test_score_detail, name="test_score_detail"),
    path('achievement/', achievement_membership, name="achievement_membership"),
    path('achievement/<pk>/', achievement_membership_detail, name="achievement_membership_detail"),
    path('work_experience/', work_experience, name="work_experience"),
    path('work_experience/<pk>/', work_experience_detail, name="work_experience_detail"),
    path('education_background/', education_background, name="education_background"),
    path('education_background/<pk>/', education_background_detail, name="education_background_detail"),    
]