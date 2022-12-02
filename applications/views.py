from collections import namedtuple
from subprocess import call
from django.conf import settings
from django.urls import reverse
from requests import request
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from applications.forms import TransactionForm
from applications.serializers import ApplicationSerializer
from applications.models import Application, Seat, Transaction
from call_applications.forms import CallForApplicationForm
from call_applications.models import CallForApplication
from functions.permissions import IsAdminOrReadOnly, IsOwnerOrAdminOrForbidden
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser
from profiles.models import *
from profiles.serializers import ProfileSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from sslcommerz_lib import SSLCOMMERZ 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import render_to_pdf, generate_zip, render_pdf, generate_roll_no
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
#@todo permissions need to be revised

@login_required()
def applications(request):
    
    if request.method == "GET":
        season = request.GET.get('season', None)
        status = request.GET.get('status', None)

        query = Q()
        if season:
            query &= Q(call_for_application=season)
        if status == "pending":
            query &= Q(is_approved=False)
        elif status == "approved":
            query &= Q(is_approved=True)

        if not request.user.is_staff:
            query &= Q(user=request.user)
        
        
        application_list = Application.objects.filter(query).prefetch_related('transaction', 'seat', 'call_for_application', 'user')

        page = request.GET.get('page', 1)
        paginator = Paginator(application_list, 10)
       
        try:
            applications = paginator.page(page)
        except PageNotAnInteger:
            applications = paginator.page(1)
        except EmptyPage:
            applications = paginator.page(paginator.num_pages)
        # serializer = ApplicationSerializer(application, many=True)
        # print(season)
        return render(request, 'applications.html', {"applications": applications, 'title': 'Applications', "filters": {"season": season, "status": status}})

@login_required()
def admit_card(request):
    if request.method == "GET":
        if request.user.is_staff:
            applications = []
            open_applications = CallForApplication.objects.all()
        else:
            applications = Application.objects.filter(is_admit_ready=False, user=request.user) 
            open_applications = []
        return render(request, 'admit_card.html', {"applications": applications, "open_applications": open_applications})
 


@login_required()
def generate_admit_card(request, pk):
    if request.user.is_staff:
        application = get_object_or_404(Application, pk=pk)
    else:
        application =  get_object_or_404(Application, pk=pk, user=request.user)
    
    if not application.seat:
        messages.error(request, "Admit Card Not Available Yet")
        return HttpResponse("Admit Card Not Available Yet")

    if request.method == "GET":

         # template = get_template('pdf/callback_report.html')
        context = {
                "application": application,
        }

        # html = template.render(context)
        pdf = render_to_pdf(request, 'pdf/admit_card.html' , context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "admit_card_%s.pdf" %(application.roll_no)
            # content = "inline; filename='%s'" %(filename)
            # download = request.GET.get("download")
            # if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


@login_required()
def generate_bulk_admit_card(request, pk):

    applications = Application.objects.filter(call_for_application=pk).prefetch_related( 'transaction', 'call_for_application', 'seat' )
    
    filetype = request.GET.get('format', 'pdf')
    
    if filetype == "zip":
        files = []
        for application in applications:
            if application.seat:
                context = {
                        "application": application,
                }
                pdf = render_pdf(request, 'pdf/admit_card.html' , context)
                files.append((application.roll_no + ".pdf", pdf))
            else:
                continue

        full_zip_in_memory = generate_zip(files)

        response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="admit_cards_{}.zip"'.format(application.call_for_application.title)

        return response

    elif filetype == "pdf":

         # template = get_template('pdf/callback_report.html')
        context = {
                "applications": [x for x in applications if x.seat],
        }

        # html = template.render(context)
        pdf = render_to_pdf(request, 'pdf/admit_card_bulk.html' , context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "admit_card_%s.pdf" %(applications[0].call_for_application.title)
            # content = "inline; filename='%s'" %(filename)
            # download = request.GET.get("download")
            # if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


@login_required()
def generate_application_form(request, pk):

    if request.user.is_staff:
        application = get_object_or_404(Application, pk=pk)
    else:
        raise Http404("Not Found")
   
    if request.method == "GET":

         # template = get_template('pdf/callback_report.html')
        context = {
                "application": application,
        }

        # html = template.render(context)
        pdf = render_to_pdf(request, 'pdf/application_form.html' , context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "application_form_%s.pdf" %(application.roll_no)
            # content = "inline; filename='%s'" %(filename)
            # download = request.GET.get("download")
            # if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


@login_required()
def generate_bulk_application_form(request, pk):
    if not request.user.is_staff:
        raise Http404("Not Found")
    
    applications = Application.objects.filter(call_for_application=pk).prefetch_related( 'transaction', 'call_for_application', 'seat' )
    
    filetype = request.GET.get('format', 'pdf')
    
    if filetype == "zip":
        files = []

        for application in applications:
            context = {
                    "application": application,
            }
            pdf = render_pdf(request, 'pdf/application_form.html' , context)
            files.append((application.roll_no + ".pdf", pdf))

        full_zip_in_memory = generate_zip(files)

        response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="application_form_{}.zip"'.format(application.call_for_application.title)

        return response
        

    elif filetype == "pdf":

         # template = get_template('pdf/callback_report.html')
        context = {
                "applications": applications,
        }

        # html = template.render(context)
        pdf = render_to_pdf(request, 'pdf/application_form_bulk.html' , context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "application_forms_%s.pdf" %(applications[0].call_for_application.title)
            # content = "inline; filename='%s'" %(filename)
            # download = request.GET.get("download")
            # if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


@login_required()
def application(request, pk):
    call_for_application = get_object_or_404(CallForApplication, pk=pk)

    ProfileData = namedtuple('ProfileData', ('basic_info', 'test_scores', 'achievements', 'work_experiences', 'educational_backgrounds', 'user'))
    try:
        profile = ProfileData(
            basic_info=BasicInfo.objects.filter(user=request.user),
            test_scores=TestScore.objects.filter(user=request.user),
            achievements=AchievementMembership.objects.filter(user=request.user),
            work_experiences=WorkExperience.objects.filter(user=request.user),
            educational_backgrounds=EducationalBackground.objects.filter(user=request.user),
            user=request.user
        )
    except Exception as e:
        print(e)
        messages.error(request, "Failed to submit form")
        return JsonResponse({"error": "Not enough data in profile"}, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == "POST":
        
        application = Application.objects.filter(user=request.user, call_for_application=call_for_application)
        if application:
            messages.error(request, "Looks like an application is already submitted")
            return JsonResponse({"status": "success", "msg": "Failed to submit the application"}, status=201)


        profile_serializer = ProfileSerializer(profile)
        
        roll_no = generate_roll_no(call_for_application)
        application = Application(
            call_for_application=call_for_application,
            data=profile_serializer.data, 
            roll_no=roll_no,
            user=request.user
            )
        application.save()
        messages.success(request, "Successfully Submitted Application")
        return JsonResponse({"status": "success", "msg": "done"}, status=201)


    elif request.method == "GET":
        return render(request, 'apply_for_call_application.html', {"season": call_for_application, "profile":profile} )


@login_required()
def application_transaction(request, pk):
    if request.user.is_staff:
        application = get_object_or_404(Application, id=pk)
    else:
        application = get_object_or_404(Application, id=pk, user=request.user)

    if request.method == "POST":

        if application.transaction:
            messages.error(request, "Unable to create entry as an entry already exists")
            err_msg = "Information Already exist"
            return JsonResponse({"status":"error", "msg": err_msg}, status=400)

        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.payment_type = "Manual"
            transaction.save()

            application.transaction = transaction
            application.is_payment_done = True
            application.save()
            
            messages.success(request, "Successfully Created Payment Entry")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)
        else:
            messages.error(request, "Failed To Create Payment Entry")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    
    elif request.method == "GET":
        transaction = application.transaction
        return render(request, 'transaction.html', {"transaction": transaction})

@login_required()
def list_transaction(request):
    if request.user.is_staff:
        transactions_list = Transaction.objects.all()
    else:
        transactions_list = Transaction.objects.filter(user=request.user)
    
    status = request.GET.get('status', None)
    season = request.GET.get('season', None)
    date = request.GET.get('date', None)
    

    query = Q()
    if status:
        if status=='pending':
            query &= Q(is_approved=False)
        elif status=='approved':
            query &= Q(is_approved=True)

    if season:
        query &= Q(application__call_for_application=season)
    
    if date:
        if date== "today":
            query &= Q(transaction_time__gte=datetime.now()-timedelta(days=1))
        elif date=="last7":
            query &= Q(transaction_time__gte=datetime.now()-timedelta(days=7))
        elif date=="last30":
            query &= Q(transaction_time__gte=datetime.now()-timedelta(days=30))
    
    transaction_list = transactions_list.filter(query).prefetch_related('application_set')

    page = request.GET.get('page', 1)
    paginator = Paginator(transaction_list, 10)
    
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)
    return render(request, 'transactions.html', {"transactions": transactions, "filters":{ "status": status, "date":date, "season":season}})

@login_required()
def transaction_detail(request, pk):
    if not request.user.is_staff:
        transaction = get_object_or_404(Transaction, id=pk, user=request.user)
    else:
        transaction = get_object_or_404(Transaction, id=pk)

    return render(request, 'transaction.html', {"transaction":transaction})


@login_required()
def manual_transaction_edit(request, pk):
    # pk = Transaction Pk
    if not request.user.is_staff:
        transaction = get_object_or_404(Transaction, id=pk, user=request.user)
    else:
        transaction = get_object_or_404(Transaction, id=pk)
    
    if request.method == "GET":
        return render(request, 'form/manual_payment_form.html', {
            "action": reverse('edit_manual_transaction_detail', args=[pk]),
            "transaction": transaction,

        })
        
    if request.method == "POST":
        transaction = TransactionForm(request.POST, instance=transaction)
        if transaction.is_valid():
            transaction.save()

            messages.success(request, "Successfully Updated Transaction Detail")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)
        else:
            messages.error(request, "Failed To Update Educational Background")
            err_msg = ""
            for field, errors in transaction.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    
    elif request.method == "DELETE":
        try:
            application = transaction.application
            application.is_payment_done = False
            application.save()
            
            transaction.delete()

            messages.success(request, "Successfully Deleted")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Delete Transaction")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)



@permission_classes([IsAuthenticated])
def application_detail(request, pk):
    if request.method == "GET":
        if request.user.is_staff:
            application = get_object_or_404(Application, pk=pk)
        else:
            application = get_object_or_404(Application, pk=pk, user=request.user)
            
        # serializer = ApplicationSerializer(application, many=True)
        return render(request, 'application_detail.html', {"application": application})


@api_view(['POST', "GET"])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FileUploadParser ])
def api_application(request):
    if request.method == "POST":
        ProfileData = namedtuple('ProfileData', ('basic_info', 'test_scores', 'achievements', 'work_experiences', 'educational_backgrounds', 'user'))
        try:
            profile = ProfileData(
                basic_info=BasicInfo.objects.filter(user=request.user),
                test_scores=TestScore.objects.filter(user=request.user),
                achievements=AchievementMembership.objects.filter(user=request.user),
                work_experiences=WorkExperience.objects.filter(user=request.user),
                educational_backgrounds=EducationalBackground.objects.filter(user=request.user),
                user=request.user
            )
        except Exception as e:
            print(e)
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
def api_application_detail(request, pk):
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
            seat = Seat.objects.create(room=room, capacity=capacity, call_for_application=call_for_application)
            seat.save()
            #@todo need to update 
            applicants = Application.objects.filter(seat__isnull =True, is_approved=False , call_for_application=call_for_application) [:capacity] 
            Application.objects.filter(id__in=applicants).update(seat=seat)

        return JsonResponse({"message": "Seat plan generated successfully"})

    elif request.method == "GET":
        values_list =  Application.objects.filter(call_for_application=call_for_application).values_list('seat', flat=True).distinct()
        seats = {}
        for value in values_list:
            seats[value if value else "Not Allocated"] = [x.roll_no for x in Application.objects.filter(seat=value)]
  
        return JsonResponse(seats, safe=False)

@login_required()
def seat_plan(request):
    if request.user.is_staff:
        if request.method == "GET":
            
            season = request.GET.get('season', None)
            if season:
                query = Q()
                season = get_object_or_404(CallForApplication, id=season)

                if season:
                    query &= Q(call_for_application=season)
                    
                applications = Application.objects.filter(query).prefetch_related('seat')
                return render(request, 'seat_plan_detail.html', {"applications": applications, "season": season })

            else:
                seasons = CallForApplication.objects.filter(start_date__lte=datetime.today(), end_date__gt=datetime.today()-timedelta(days=30)).prefetch_related('application_set')
                data = {}
                for season in seasons:
                    # applications = season.application_set.all().values_list('id')

                    # seats  = Seat.objects.filter(application_set__is_null=False, application_set__in=application())
                    seats = Seat.objects.filter(call_for_application=season).prefetch_related('application_set')
                    data[season] = {
                        "seats": {x.room: len(x.application_set.all()) for x in seats},
                        "num_applicants" : len(season.application_set.all()),
                        "unallocated" : len(season.application_set.all().filter(seat__isnull=True))
                    }
                    
                print(data)
                applications = []

                return render(request, 'seat_plan.html', {"applications": applications, "seasons": data })
        
        
@login_required()
def seat_plan_detail(request, pk):
    if request.user.is_staff:

        if request.method == "POST":
            season = get_object_or_404(CallForApplication, id=pk)
            data = request.POST
            rooms_and_capacities = []
            for key, value in data.items():
                if "room" in key:
                    suffix = key.replace('room', "")
                    try:
                        capacity = int(data.get('capacity'+suffix, 0))
                    except:
                        capacity = 0
            
                    rooms_and_capacities.append([value, capacity])
            print(rooms_and_capacities)
            for av in rooms_and_capacities:
                room = av[0]
                capacity = int(av[1])
                
                if capacity != 0:
                    seat = Seat.objects.create(room=room, capacity=int(av[1]), call_for_application=season)
                    seat.save()
                    print("saved", seat)
                    #@todo change is_approved to True 
                    applicants = Application.objects.filter(seat__isnull =True, is_approved=True , call_for_application=season) [:capacity] 
                    a = Application.objects.filter(id__in=applicants).update(seat=seat)
                    print("updated", a)

            messages.success(request, "Successfully Allocated Seat")
            return JsonResponse({"status": "success", "msg": "done"}, status=201)
        if request.method == "DELETE":
            seat = get_object_or_404(Seat, id=pk)
            # seat.application_set.all().update(seat=None)
            seat.delete()
            messages.success(request, "Successfully Deleted Seat")
            return JsonResponse({"status": "success", "msg": "done"}, status=201)

    messages.success(request, "Failed to generate seat plan")
    return JsonResponse({"status": "error", "msg": "Something is Wrong"}, status=201)
