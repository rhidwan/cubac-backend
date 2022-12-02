from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from call_applications.models import CallForApplication
from applications.models import Application, Transaction
from datetime import datetime, timedelta
# Create your views here.

@login_required()
def home(request):
    if request.user.is_staff:
        open_applications = CallForApplication.objects.filter(start_date__lte=datetime.today(), end_date__gt=datetime.today()-timedelta(days=60))
        applications = []
        return render(request, 'index.html', {"open_applications": open_applications})

    else:
        applications = Application.objects.filter(user=request.user)
        transactions = [x.transaction for x in applications if x.transaction]
        open_applications = []

        return render(request, 'index.html', {"open_applications": open_applications, "applications": applications, "transactions":transactions})

def bkash(request):
    return render(request, 'bkash.html')
