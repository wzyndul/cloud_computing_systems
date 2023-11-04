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

# Main page
def index_page(request):
    return render(request, 'index.html')


# Registering users
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('index_page')

        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')

    form = UserRegistrationForm()
    return render(request, 'register.html', {'register_form': form})


# Logging in users
def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect('index_page')
            else:
                print("No such user")
                messages.error(request, "Invalid username or password.")

        else:
            print("Invalid form")
            messages.error(request, "Invalid username or password.")

    elif request.method == 'GET':
        if request.user.is_authenticated:
            messages.success(request, f"You are already logged in as {request.user.username}.")
            return redirect('index_page')

    form = UserLoginForm()
    return render(request, 'login.html', {'login_form': form})


# Logging out users
def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index_page')


def success_page(request):
    users = User.objects.all()  # Retrieve all users
    return render(request, 'success.html', {'users': users})
