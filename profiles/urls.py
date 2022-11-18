from re import M
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('basic_info/create/', create_basic_info, name="create_basic_info"),
    path('', profile, name="profile"),
    path('api/', user_detail, name="user_detail"),

    path('basic_info/', basic_info, name="basic_info"),
    path('test_score/', test_score, name="test_score"),
    path('achievement/',  achievement_membership, name="achievement_membership"),
    path('work_experience/', work_experience, name="work_experience"),
    path('education_background/', educational_background, name="education_background"),
    path('education_background/<pk>/', edit_educational_background_detail, name="edit_educational_background_detail"),
    path('work_experience/<pk>/', edit_work_experience_detail, name="edit_work_experience_detail"),
    path('test_score/<pk>/', edit_test_score_detail, name="edit_test_score_detail"),
    path('achievement/<pk>/',edit_achievement_membership_detail, name="edit_achievement_membership_detail" ),



    path('api/basic_info/', basic_info_detail, name="basic_info_detail"),
    path('api/test_score/', api_test_score, name="test_score_api"),
    path('api/test_score/<pk>/', test_score_detail, name="test_score_detail"),
    path('api/achievement/', api_achievement_membership, name="achievement_membership_api"),
    path('api/achievement/<pk>/', achievement_membership_detail, name="achievement_membership_detail"),
    path('api/work_experience/', api_work_experience, name="work_experience_api"),
    path('api/work_experience/<pk>/', work_experience_detail, name="work_experience_detail"),
    path('api/education_background/', education_background, name="education_background_api"),
    path('api/education_background/<pk>/', education_background_detail, name="education_background_detail"),    
]