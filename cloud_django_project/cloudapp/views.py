from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from cloud_django_project.forms import UserRegistrationForm, UserLoginForm
from cloudapp import blob_handler


# Main page
def index_page(request):
    return render(request, 'index.html')


# Registering users
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            blob_handler.create_blob_container(user)
            messages.success(request, 'Registration successful.')
            login(request, user)
            return redirect('index_page')

        else:
            messages.error(request,
                           'Unsuccessful registration. Invalid information.')

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
                messages.success(request,
                                 f"You are now logged in as {username}.")
                login(request, user)
                return redirect('index_page')
            else:
                messages.error(request, "Invalid username or password.")

        else:
            messages.error(request, "Invalid username or password.")

    elif request.method == 'GET':
        if request.user.is_authenticated:
            messages.success(request,
                             f"You are already logged in as {request.user.username}.")
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


def upload_file(request):
    return render(request, 'storage.html')

def storage(request):
    if request.method == 'GET':
        blobs = blob_handler.list_blobs(request.user)
        return render(request, 'storage.html', {'blobs': blobs})

    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')

        for uploaded_file in uploaded_files:
            blob_handler.upload_blob(request.user, uploaded_file)

        messages.success(request, f'{len(uploaded_files)} file(s) uploaded successfully.')
        return redirect('storage')

    return render(request, 'storage.html')
