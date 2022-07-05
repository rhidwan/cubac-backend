from django.shortcuts import render

from call_applications.serializers import CallForApplicationSerializer
from .models import CallForApplication
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from functions.permissions import IsAdminOrReadOnly
from datetime import datetime, timedelta
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser

# Create your views here.
@api_view(['POST', "GET"])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
def open_application(request):
    if request.method == "POST":
        if request.user.is_staff == True:
            serializer = CallForApplicationSerializer(data=request.data, context={'request' : request})
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"error": "You don't have permission to perform this action"}, status=403)
   
    elif request.method == "GET":
        if request.user.is_staff == True:
            open_applications = CallForApplication.objects.filter(end_date__gt=datetime.today() - timedelta(days=3))
        else:
            open_applications = CallForApplication.objects.filter(is_open=True)
       
        serializer = CallForApplicationSerializer(open_applications, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
def application_detail(request, pk):
    try:
        open_application = CallForApplication.objects.get(pk=pk)
    except:
        return JsonResponse({'error': "Not Found"}, status=404)

    if request.method == "GET":
        serializer = CallForApplicationSerializer(open_application)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT': 

        open_applicatioon_serializer = CallForApplicationSerializer(open_application, data=request.data, partial=True )
        if open_applicatioon_serializer.is_valid(): 
            open_applicatioon_serializer.save() 
            return JsonResponse(open_applicatioon_serializer.data) 
        return JsonResponse(open_applicatioon_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        open_application.delete() 
        return JsonResponse({'message': 'Open For Application deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


