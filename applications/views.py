from collections import namedtuple
from subprocess import call
from django.conf import settings
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from applications.serializers import ApplicationSerializer
from applications.models import Application
from call_applications.models import CallForApplication
from functions.permissions import IsAdminOrReadOnly, IsOwnerOrAdminOrForbidden
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser
from profiles.models import *
from profiles.serializers import ProfileSerializer
from django.db.models import Q

from sslcommerz_lib import SSLCOMMERZ 
from decimal import Decimal

# Create your views here.
#@todo permissions need to be revised

def generate_roll_no(call_application):
    '''
    Helper function to generate roll number
    input: 
        -  Call Application Object
    output :
        - Generated Roll Number 
    '''
    
    applications = Application.objects.filter(call_for_application=call_application)

    short_code = call_application.shortcode 
    suffix = len(applications) + 1
    roll_number = short_code + str(suffix).zfill(4)

    return roll_number

    
@api_view(['POST', "GET"])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
def application(request):
    if request.method == "POST":
        ProfileData = namedtuple('ProfileData', ('basic_info', 'test_scores', 'achievements', 'work_experiences', 'educational_backgrounds'))
        try:
            profile = ProfileData(
                basic_info=BasicInfo.objects.get(user=request.user),
                test_scores=TestScore.objects.filter(user=request.user),
                achievements=AchievementMembership.objects.filter(user=request.user),
                work_experiences=WorkExperience.objects.filter(user=request.user),
                educational_backgrounds=EducationalBackground.objects.filter(user=request.user)
            )
        except:
            return JsonResponse({"error": "Not enough data in profile"}, status=status.HTTP_400_BAD_REQUEST)
        profile_serializer = ProfileSerializer(profile)
    
        serializer = ApplicationSerializer(data=request.data, context={'request' : request})
        if serializer.is_valid():
            roll_no = generate_roll_no(serializer.validated_data["call_for_application"])
            serializer.save(data=profile_serializer.data, roll_no=roll_no)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "GET":
        application = Application.objects.filter(user=request.user)
        serializer = ApplicationSerializer(application, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly, IsOwnerOrAdminOrForbidden])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
def application_detail(request, pk):
    try:
        application = Application.objects.get(pk=pk)
    except:
        return JsonResponse({'error': "Not Found"}, status=404)

    if request.method == "GET":
        serializer = ApplicationSerializer(application)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT': 
        applicatioon_serializer = ApplicationSerializer(application, data=request.data, partial=True )
        if applicatioon_serializer.is_valid(): 
            applicatioon_serializer.save() 
            return JsonResponse(applicatioon_serializer.data) 
        return JsonResponse(applicatioon_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        application.delete() 
        return JsonResponse({'message': 'Application deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
def initiate_payment(request, app_id):
    try:
        application = Application.objects.get(pk=app_id)
    except:
        return JsonResponse({'error': "Application Not Found"}, status=404)

    if application.is_payment_done :
        return JsonResponse({"error": "Payemnt Already done"}, status=400)

    basic_info = BasicInfo.objects.get(user=request.user)
    status_url = request.build_absolute_uri(reverse('process_payment_update'))

    ssl_conf = { 'store_id': settings.SSL_STORE_ID , 'store_pass': settings.SSL_STORE_SECRET, 'issandbox': True }
    sslcz = SSLCOMMERZ(ssl_conf)
    
    post_body = {}
    post_body['total_amount'] = 520.50
    post_body['currency'] = "BDT"
    post_body['tran_id'] = app_id
    post_body['success_url'] = status_url
    post_body['fail_url'] = status_url
    post_body['cancel_url'] = status_url
    post_body["ipn_url"] = status_url
    post_body['emi_option'] = 0
    post_body['cus_name'] = request.user.full_name
    post_body['cus_email'] = request.user.email
    post_body['cus_phone'] = basic_info.phone_number
    post_body['cus_add1'] = basic_info.present_address
    post_body['cus_city'] = "Chittagong"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "CUBAC FEE"
    post_body['product_category'] = "Digital"
    post_body['product_profile'] = "Digital"

    response = sslcz.createSession(post_body)
    return JsonResponse(response)

@api_view(['POST'])
def process_payment_update(request):
    data = request.POST

    tran_id = data["tran_id"]
    val_id = data["val_id"]
    status = data["status"]

    print(data)

    if status == "VALID":
        application = Application.objects.get(pk=tran_id)
        application.is_payment_done = True
        application.gw_trx_id = val_id
        application.save()

    return JsonResponse({'message': 'Payment Successful!'})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
def generate_seat_plan(request, pk):
    call_for_application = CallForApplication.objects.get(pk=pk)

    if request.method == "POST":
        data = request.data
        #available room should be of [['room': 10]] format, Room name and capacity
   
        rooms_and_capacities = data.get("rooms_and_capacities", [])

        if type(rooms_and_capacities) != list or rooms_and_capacities == []:
            return JsonResponse({"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

        for av in rooms_and_capacities:
            room = av[0]
            capacity = int(av[1])
            #@todo change is_approved to True 
            applicants = Application.objects.filter(seat__isnull =True, is_approved=False , call_for_application=call_for_application) [:capacity] 
            Application.objects.filter(id__in=applicants).update(seat=room)

        return JsonResponse({"message": "Seat plan generated successfully"})

    elif request.method == "GET":
        values_list =  Application.objects.filter(call_for_application=call_for_application).values_list('seat', flat=True).distinct()
        seats = {}
        for value in values_list:
            seats[value if value else "Not Allocated"] = [x.roll_no for x in Application.objects.filter(seat=value)]
  
        return JsonResponse(seats, safe=False)