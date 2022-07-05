from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def bkash(request):
    return render(request, 'bkash.html')