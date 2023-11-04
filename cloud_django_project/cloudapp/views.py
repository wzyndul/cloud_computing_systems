from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from cloud_django_project.forms import UserRegistrationForm, UserLoginForm


# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             if 'login' in request.POST:
#                 username = request.POST['username']
#                 password = request.POST['password']
#                 user = authenticate(username=username, password=password)
#                 if user:
#                     return redirect('success_page')
#                 else:
#                     return HttpResponse('Invalid login credentials')
#
#             elif 'register' in request.POST:
#                 form.save()  # This will create a new user
#                 # Redirect the user to a success page or any other appropriate action
#                 return redirect('success_page')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'register.html', {'form': form})

def index_page(request):
    return render(request, 'index.html')


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('success_page')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    form = UserRegistrationForm()
    return render(request, 'register.html', {'register_form': form})


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                print(f"User authenticated: {user.username}")
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('success_page')
            else:
                print(f"User not authenticated: {user.username}")
                messages.error(request, "Invalid username or password.")

        else:
            print("Idk what happened")
            messages.error(request, "Invalid username or password.")

    elif request.method == 'GET':
        if request.user.is_authenticated:
            messages.info(request, f"You are already logged in as {request.user.username}.")
            return redirect('success_page')

        form = UserLoginForm()
        return render(request, 'login.html', {'login_form': form})


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index_page')


def success_page(request):
    users = User.objects.all()  # Retrieve all users
    return render(request, 'success.html', {'users': users})
