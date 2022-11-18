from cProfile import Profile
from collections import namedtuple
from urllib import response
from django.db import IntegrityError
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser
from rest_framework import status
from urllib3 import HTTPResponse
from profiles.models import AchievementMembership, BasicInfo, EducationalBackground, WorkExperience
from django.shortcuts import render
from profiles.serializers import AchievementMembershipSerializer, BasicInfoSerializer, EducationalBackgroundSerializer, ProfileSerializer, TestScoreSerializer, WorkExperienceSerializer
from profiles.models import TestScore, BasicInfo
from user.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import * 
import os
from django.shortcuts import get_object_or_404


@permission_classes([IsAuthenticated])
def profile(request):
    ProfileData = namedtuple('ProfileData', ('basic_info', 'test_scores', 'achievements', 'work_experiences', 'educational_backgrounds', 'user'))

    profile = ProfileData(
        basic_info=BasicInfo.objects.filter(user=request.user),
        test_scores=TestScore.objects.filter(user=request.user),
        achievements=AchievementMembership.objects.filter(user=request.user),
        work_experiences=WorkExperience.objects.filter(user=request.user),
        educational_backgrounds=EducationalBackground.objects.filter(user=request.user),
        user=request.user
    )
    profile_serializer = ProfileSerializer(profile)
    # print(profile_serializer.data)
    return render(request, 'profile.html', {"profile": profile_serializer.data})

@login_required()
def basic_info(request):
    if request.method == "POST":
        try:
            basic_info = BasicInfo.objects.get(user=request.user)
            form = BasicInfoForm(request.POST, instance=basic_info)
        except Exception as e:
            form = BasicInfoForm(request.POST)

        try:
            photo_path = basic_info.photo.path
        except Exception as e:
            print(e)
            photo_path = None

        if form.is_valid():
            photo = request.FILES.get('photo')
            basic_info = form.save(commit=False)
            if photo:
                try:os.remove(photo_path)
                except:pass
                basic_info.photo = photo
            
            try:
                basic_info.user
            except:
                basic_info.user = request.user
            
            basic_info.save()

        else:
        
            messages.error(request, "Failed To Update Information")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)

        messages.success(request, "Successfully updated information")
        return JsonResponse({"status": "success", "msg": "Done."}, status=201)

@login_required()
def work_experience(request):
    if request.method == "POST":
      
        form = WorkExperienceForm(request.POST)

        if form.is_valid():
            work_experience = form.save(commit=False)
            work_experience.user = request.user
            work_experience.save()
            messages.success(request, "Successfully Created Work Experience")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)
        else:
            messages.error(request, "Failed To Create Work Experience")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)

@login_required()
def educational_background(request):
    if request.method == "POST":
      
        form = EducationalBackgroundForm(request.POST)

        if form.is_valid():
            education_background = form.save(commit=False)
            education_background.user = request.user
            education_background.save()

            messages.success(request, "Successfully Created Educational background")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)
        else:
            messages.error(request, "Failed To Create Educational Background")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)

@login_required()
def edit_educational_background_detail(request, pk):
    education_backgroud = get_object_or_404(EducationalBackground, id=pk, user=request.user)
    if request.method == "GET":
        return render(request, 'form/educational_background_form.html', {
            "action": reverse('edit_educational_background_detail', args=[pk]),
            "education_background": education_backgroud,

        })
    if request.method == "POST":
        form = EducationalBackgroundForm(request.POST, instance=education_backgroud)
        if form.is_valid():
            form.save()

            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update Educational Background")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    if request.method == "DELETE":
        try:
            education_backgroud.delete()
            
            messages.success(request, "Successfully Deleted")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Update Educational Background")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)

@login_required()
def edit_work_experience_detail(request, pk):
    work_experience = get_object_or_404(WorkExperience, id=pk, user=request.user)
    if request.method == "GET":
        return render(request, 'form/work_experience_form.html', {
            "action": reverse('edit_work_experience_detail', args=[pk]),
            "work_experience": work_experience,

        })
    if request.method == "POST":
        form = WorkExperienceForm(request.POST, instance=work_experience)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update Work Experience")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    if request.method == "DELETE":
        try:
            work_experience.delete()
            
            messages.success(request, "Successfully Deleted")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Update Work Experience")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)

@login_required()
def edit_test_score_detail(request, pk):
    test_score = get_object_or_404(TestScore, id=pk, user=request.user)
    if request.method == "GET":
        return render(request, 'form/test_score_form.html', {
            "action": reverse('edit_test_score_detail', args=[pk]),
            "test_score": test_score,

        })
    if request.method == "POST":
        form = TestScoreForm(request.POST, instance=test_score)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update Test Score")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    if request.method == "DELETE":
        try:
            test_score.delete()
            
            messages.success(request, "Successfully Deleted")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Delete Test Score")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)

@login_required()
def edit_achievement_membership_detail(request, pk):
    achievement_membership = get_object_or_404(AchievementMembership, id=pk, user=request.user)
    if request.method == "GET":
        return render(request, 'form/achievement_membership_form.html', {
            "action": reverse('edit_achievement_membership_detail', args=[pk]),
            "achievement_membership": achievement_membership,

        })
    if request.method == "POST":
        form = AchievementMembershipForm(request.POST, instance=achievement_membership)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update Achievement Entry")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    if request.method == "DELETE":
        try:
            achievement_membership.delete()
            
            messages.success(request, "Successfully Deleted")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Update Achievement Entry")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)



@login_required()
def test_score(request):
    if request.method == "POST":
      
        form = TestScoreForm(request.POST)

        if form.is_valid():
            test_score = form.save(commit=False)
            test_score.user = request.user
            test_score.save()
            
            messages.success(request, "Successfully Created Test Entry")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)
        else:
            messages.error(request, "Failed To Create Test Score")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)


@login_required()
def achievement_membership(request):
    if request.method == "POST":
      
        form = AchievementMembershipForm(request.POST)

        if form.is_valid():
            achievement_membership = form.save(commit=False)
            achievement_membership.user = request.user
            achievement_membership.save()
            
            messages.success(request, "Successfully Created Achievement/Membership Entry")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)
        else:
            print(form.errors)
            messages.error(request, "Failed To Create Entry")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)


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
def api_test_score(request):
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
def api_achievement_membership(request):
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
def api_work_experience(request):
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
    ProfileData = namedtuple('ProfileData', ('basic_info', 'test_scores', 'achievements', 'work_experiences', 'educational_backgrounds', 'user'))

    profile = ProfileData(
        basic_info=BasicInfo.objects.get(user=request.user),
        test_scores=TestScore.objects.filter(user=request.user),
        achievements=AchievementMembership.objects.filter(user=request.user),
        work_experiences=WorkExperience.objects.filter(user=request.user),
        educational_backgrounds=EducationalBackground.objects.filter(user=request.user),
        user=request.user
    )

    profile_serializer = ProfileSerializer(profile)
    return JsonResponse(profile_serializer.data)