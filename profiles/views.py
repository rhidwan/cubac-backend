from cProfile import Profile
from collections import namedtuple
from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser
from rest_framework import status
from profiles.models import AchievementMembership, BasicInfo, EducationalBackground, WorkExperience

from profiles.serializers import AchievementMembershipSerializer, BasicInfoSerializer, EducationalBackgroundSerializer, ProfileSerializer, TestScoreSerializer, WorkExperienceSerializer
from profiles.models import TestScore, BasicInfo
from user.models import User

@api_view(["GET", "PUT", "POST"])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
@permission_classes([IsAuthenticated])
def basic_info_detail(request):
    try:
        basic_info = BasicInfo.objects.get(user=request.user)
    except:
        return JsonResponse({'error': "Not Found"}, status=404)

    if request.method == "GET":
        serializer = BasicInfoSerializer(basic_info)
        return JsonResponse(serializer.data)
    
    elif request.method == "POST":
        serializer = BasicInfoSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                return JsonResponse({"error": "Can't create duplicate Entry!"}, status=409)
            except:
                return JsonResponse({"error":"Something Went wrong"}, status=409)
            return JsonResponse(serializer.errors, status=201)
        return JsonResponse(serializer.errors, status=400)
   
    elif request.method == 'PUT': 
       
        basic_info_serializer = BasicInfoSerializer(basic_info, data=request.data, partial=True )
        if basic_info_serializer.is_valid(): 
            basic_info_serializer.save() 
            return JsonResponse(basic_info_serializer.data) 
        return JsonResponse(basic_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 

#Test Score Views
@api_view(['GET', 'POST'])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
@permission_classes([IsAuthenticated])
def test_score(request):
    if request.method == "POST":
        serializer = TestScoreSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "GET":
        test_scores = TestScore.objects.filter(user=request.user)
        test_scores_serializer = TestScoreSerializer(test_scores, many=True)
        return JsonResponse(test_scores_serializer.data, safe=False ) 


@api_view(["GET", "PUT", "DELETE"])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
@permission_classes([IsAuthenticated])
def test_score_detail(request, pk):
    try:
        test_score = TestScore.objects.get(pk=pk)
    except:
        return JsonResponse({'error': "Not Found"}, status=404)

    if request.method == "GET":
        serializer = TestScoreSerializer(test_score)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT': 
       
        test_score_serializer = TestScoreSerializer(test_score, data=request.data, partial=True )
        if test_score_serializer.is_valid(): 
            test_score_serializer.save() 
            return JsonResponse(test_score_serializer.data) 
        return JsonResponse(test_score_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        test_score.delete() 
        return JsonResponse({'message': 'Test Score Entry deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

#Achievement Membership Views
@api_view(['POST', "GET"])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
@permission_classes([IsAuthenticated])
def achievement_membership(request):
    if request.method == "POST":
        serializer = AchievementMembershipSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "GET":
        achievements = AchievementMembership.objects.filter(user=request.user)
        achievements_serializer = AchievementMembershipSerializer(achievements, many=True)
        return JsonResponse(achievements_serializer.data, safe=False ) 



@api_view(["GET", "PUT", "DELETE"])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
@permission_classes([IsAuthenticated])
def achievement_membership_detail(request, pk):
    try:
        achivement_membership = AchievementMembership.objects.get(pk=pk)
    except:
        return JsonResponse({'error': "Not Found"}, status=404)

    if request.method == "GET":
        serializer = AchievementMembershipSerializer(achivement_membership)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT': 
       
        achievement_membership_serializer = AchievementMembershipSerializer(achivement_membership, data=request.data, partial=True )
        if achievement_membership_serializer.is_valid(): 
            achievement_membership_serializer.save() 
            return JsonResponse(achievement_membership_serializer.data) 
        return JsonResponse(achievement_membership_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        achivement_membership.delete() 
        return JsonResponse({'message': 'Achievement Mebership Entry deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


#work Experience views

@api_view(['POST', "GET"])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
@permission_classes([IsAuthenticated])
def work_experience(request):
    if request.method == "POST":
        serializer = WorkExperienceSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == "GET":
        work_experiences = WorkExperience.objects.filter(user=request.user)
        work_experiences_serializer = WorkExperienceSerializer(work_experiences, many=True)
        return JsonResponse(work_experiences_serializer.data, safe=False ) 


@api_view(["GET", "PUT", "DELETE"])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
@permission_classes([IsAuthenticated])
def work_experience_detail(request, pk):
    try:
        work_experience = WorkExperience.objects.get(pk=pk)
    except:
        return JsonResponse({'error': "Not Found"}, status=404)

    if request.method == "GET":
        serializer = WorkExperienceSerializer(work_experience)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT': 
       
        work_experience_seralizer = WorkExperienceSerializer(work_experience, data=request.data, partial=True )
        if work_experience_seralizer.is_valid(): 
            work_experience_seralizer.save() 
            return JsonResponse(work_experience_seralizer.data) 
        return JsonResponse(work_experience_seralizer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        work_experience.delete() 
        return JsonResponse({'message': 'WorK Experience Entry deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


#educational background Viewer
@api_view(['POST', "GET"])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
@permission_classes([IsAuthenticated])
def education_background(request):
    if request.method == "POST":
        serializer = EducationalBackgroundSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "GET":
        educations = EducationalBackground.objects.filter(user=request.user)
        educations_serializer = EducationalBackgroundSerializer(educations, many=True)
        return JsonResponse(educations_serializer.data, safe=False ) 


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
def education_background_detail(request, pk):
    try:
        education_background = EducationalBackground.objects.get(pk=pk)
    except:
        return JsonResponse({'error': "Not Found"}, status=404)

    if request.method == "GET":
        serializer = EducationalBackgroundSerializer(education_background)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT': 
       
        education_background_serializer = EducationalBackgroundSerializer(education_background, data=request.data, partial=True )
        if education_background_serializer.is_valid(): 
            education_background_serializer.save() 
            return JsonResponse(education_background_serializer.data) 
        return JsonResponse(education_background_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        education_background.delete() 
        return JsonResponse({'message': 'Education Background deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_detail(request):
    ProfileData = namedtuple('ProfileData', ('basic_info', 'test_scores', 'achievements', 'work_experiences', 'educational_backgrounds'))

    profile = ProfileData(
        basic_info=BasicInfo.objects.get(user=request.user),
        test_scores=TestScore.objects.filter(user=request.user),
        achievements=AchievementMembership.objects.filter(user=request.user),
        work_experiences=WorkExperience.objects.filter(user=request.user),
        educational_backgrounds=EducationalBackground.objects.filter(user=request.user)
    )

    profile_serializer = ProfileSerializer(profile)
    return JsonResponse(profile_serializer.data)