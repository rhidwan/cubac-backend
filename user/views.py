from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ClientUserCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        mobile_no = request.POST.get('mobile_no')
        password = request.POST.get('password')
        user = authenticate(mobile_no=mobile_no, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                return render(request, 'login.html', {"error": "Something Went Wrong, Please Try again later or Contact Support"})
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(mobile_no,password))
            return render(request, 'login.html', {"error": "Invalid login details given"})
    else:
        return render(request, 'login.html', {})

@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url="/login/")
def create_client(request):
    if request.method == "POST":
        form = ClientUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cient Created successfully')
            return redirect('dashboard_project')
    else:
        form = ClientUserCreationForm()

    return render(request, 'client_create.html', {"form":form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Something went wrong, Please try again')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {
        'form': form
    })