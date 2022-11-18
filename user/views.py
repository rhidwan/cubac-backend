from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from user.models import User

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request,user)
                messages.success(request, 'logged in successfully')
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                return render(request, 'login.html', {"error": "Something Went Wrong, Please Try again later or Contact Support"})
        else:
            print("Someone tried to login and failed.")
            print("They used email: {} and password: {}".format(email,password))
            return render(request, 'login.html', {"error": "Invalid login details given"})
    else:
        return render(request, 'login.html', {})

def user_registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Created successfully')
            return redirect('dashboard')
        else:
            messages.error(request, "Failed to sign Up")
            return render(request, 'signup.html', {"error": form.errors})
        #

    return render(request, 'signup.html', {})

@login_required()
def update_user_info(request):
    if request.method == "GET":
        return render(request, 'update_user_info.html')
    elif request.method == "POST" :
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Updated successfully')
            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update User Info")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    

@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url="/login/")
def make_staff_account(request):
    if request.user.is_staff:
        if request.method == "POST":
            email = request.POST.get("email", None)
            users = User.objects.filter(email = email)
            if users:
                user = users[0]
                user.is_staff = True
                user.save()

                messages.success(request, 'staff Created Successfully')
            else:
                messages.error(request, "Email Not Found")
      
    return render(request, 'staff_create.html')
  

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