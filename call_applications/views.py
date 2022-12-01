from django.shortcuts import get_object_or_404, render
from applications.models import Application, Transaction
from django.urls import reverse
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
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from call_applications.forms import CallForApplicationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
@login_required()
def open_application(request):
    if request.method == "POST":
        if request.user.is_staff == True:
            form = CallForApplicationForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Created Season")
                return JsonResponse({"status": "success", "msg": "Done."}, status=201)
            else:
                messages.error(request, "Failed To Create Season")
                err_msg = ""
                for field, errors in form.errors.items():
                    for error in errors:
                        err_msg += "\n{} - {}".format(field, error)
                return JsonResponse({"status":"error", "msg": err_msg}, status=200)
        else:
            return JsonResponse({"error": "You don't have permission to perform this action"}, status=403)
   
    elif request.method == "GET":
        

        if request.user.is_staff == True:
            seasons = request.GET.get('seasons', 'All')
            # open_applications = CallForApplication.objects.filter(end_date__gt=datetime.today() - timedelta(days=3))
            if seasons == "All":
                open_applications_list = CallForApplication.objects.all()
            elif seasons=="Open":
                open_applications_list = CallForApplication.objects.filter(start_date__lte=datetime.today(), end_date__gt=datetime.today())
            elif seasons == "Closed":
                open_applications_list = CallForApplication.objects.filter(start_date__lte=datetime.today(), end_date__lte=datetime.today())
            else:
                open_applications_list = []

        else:
            seasons = "open"
            open_applications_list = CallForApplication.objects.filter(start_date__lte=datetime.today(), end_date__gt=datetime.today())

        page = request.GET.get('page', 1)
        paginator = Paginator(open_applications_list, 10)
        
        try:
            open_applications = paginator.page(page)
        except PageNotAnInteger:
            open_applications = paginator.page(1)
        except EmptyPage:
            open_applications = paginator.page(paginator.num_pages)

        return render(request, 'seasons.html', {"open_applications": open_applications, "filters": {"seasons": seasons}})


def open_application_detail(request, slug):
   
    open_application = get_object_or_404(CallForApplication, slug=slug)
    
    if request.method == "GET":
        if request.user.is_authenticated:
            if request.user.is_staff:
                applications = Application.objects.filter(call_for_application=open_application)
                # number_of_applicants =  1 Pending Approval: 1 Payment Done: 1
                num_applications = len(applications)
                seat_allocated = len([x for x in applications if x.seat])
                payment_done = len([x for x in applications if x.is_payment_done])

                return render(request, 'season.html', {
                    "open_application": open_application,
                    "num_applicants": num_applications,
                    "seat_allocated": seat_allocated,
                    "payment_done":payment_done
                    
                    })
            else:
                applications = Application.objects.filter(call_for_application=open_application, user=request.user)
                transactions = Transaction.objects.filter(application__in=applications)
                print(applications)
                return render(request, 'season.html', {
                    "open_application": open_application,
                    "applications": applications,
                    "transactions": transactions
                    })
        else:
            return render(request, 'season_guest.html', {
                    "open_application": open_application,
                  
                    })

@login_required()
def edit_open_application_detail(request, pk):
    if request.user.is_staff:
        open_application = get_object_or_404(CallForApplication, pk=pk)

        if request.method == "GET":
            return render(request, 'form/call_application_form.html', {
                "action": reverse('edit_open_application_detail', args=[pk]),
                "call_application": open_application,
            })
        
        if request.method == "POST":
            form = CallForApplicationForm(request.POST, instance=open_application)

            if form.is_valid():
                form.save()

                messages.success(request, "Successfully Updated")
                return JsonResponse({"status": "success", "msg": "Done."}, status=201)

            else:
                messages.error(request, "Failed To Update Season")
                err_msg = ""
                for field, errors in form.errors.items():
                    for error in errors:
                        err_msg += "\n{} - {}".format(field, error)
                return JsonResponse({"status":"error", "msg": err_msg}, status=200)
        if request.method == "DELETE":
            try:
                open_application.delete()
                
                messages.success(request, "Successfully Deleted")
                return JsonResponse({"status": "success", "msg": "Done."}, status=200)
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Delete Season")
                return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)

# Create your views here.
@api_view(['POST', "GET"])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
def api_open_application(request):
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
            open_applications = CallForApplication.objects.filter(start_date__lte=datetime.today(), end_date__gte=datetime.today())
       
        serializer = CallForApplicationSerializer(open_applications, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
def api_application_detail(request, pk):
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


