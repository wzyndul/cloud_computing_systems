from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from cloud_django_project.forms import UserRegistrationForm, UserLoginForm
from cloudapp import blob_handler
from cloudapp.utils import authenticate_user
from cloudapp.utils import logger


def index_page(request):
    return render(request, 'index.html')


# Registering users
def register_user(request):
    if request.method == 'POST':
        try:
            form = UserRegistrationForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                blob_handler.create_blob_container(user)
                messages.success(request, 'Registration successful.')
                login(request, user)
                logger.info(f'New user registered: {user.username}')
                return redirect('index_page')

            else:
                messages.warning(request,'Unsuccessful registration. Invalid information.')
        except Exception as e:
            messages.error(request, "Internal Server Error. Please try again later.")
            return render(request, 'error_page.html', {'error_message': "Internal Server Error."})


    form = UserRegistrationForm()
    return render(request, 'register.html', {'register_form': form})


# Logging in users
def login_user(request):
    if request.method == 'POST':
        try:
            form = UserLoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user:
                    messages.success(request,
                                    f"You are now logged in as {username}.")
                    login(request, user)
                    logger.info(f'User logged in: {username}')
                    return redirect('index_page')
                else:
                    messages.warning(request, "Invalid username or password.")

            else:
                messages.warning(request, "Invalid username or password.")
        except Exception as e:
            messages.error(request, "Internal Server Error. Please try again later.")
            return render(request, 'error_page.html', {'error_message': "Internal Server Error."})

    elif request.method == 'GET':
        if request.user.is_authenticated:
            messages.success(request,
                             f"You are already logged in as {request.user.username}.")
            return redirect('index_page')

    form = UserLoginForm()
    return render(request, 'login.html', {'login_form': form})


# Logging out users
def logout_user(request):
    try:
        username = request.user.username
        logout(request)
        messages.info(request, "You have successfully logged out.")
        logger.info(f'User logged out: {username}')
        return redirect('index_page')
    except Exception as e:
        messages.error(request, "Internal Server Error. Please try again later.")
        return render(request, 'error_page.html', {'error_message': "Internal Server Error."})


@authenticate_user
def storage(request):
    if request.method == 'GET':
        try:
            blobs = blob_handler.list_blobs_with_properties(request.user)
            return render(request, 'storage.html', {'blobs': blobs})
        except Exception as e:
            messages.error(request, "Internal Server Error. Please try again later.")
            return render(request, 'error_page.html', {'error_message': "Internal Server Error."})
    elif request.method == 'POST':
        try:
            uploaded_files = request.FILES.getlist('files')

            blob_handler.parallel_upload_blob(request.user, uploaded_files)

            messages.success(request, f'{len(uploaded_files)} file(s) uploaded successfully.')
            return redirect('storage')
        except Exception as e:
            messages.error(request, "Internal Server Error. Please try again later.")
            return render(request, 'error_page.html', {'error_message': "Internal Server Error."})

    return render(request, 'storage.html')


@authenticate_user
def change_version(request):
    if request.method == 'POST':
        try:
            file_name = request.POST.get('file_name')
            version = request.POST.get('version')
            blob_handler.change_blob_version(request.user, file_name, version)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            messages.error(request, "Internal Server Error. Please try again later.")
            return render(request, 'error_page.html', {'error_message': "Internal Server Error."})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@authenticate_user
def download_file(request):
    if request.method == 'GET':
        file_name = request.GET.get('file_name')
        try:
            response = blob_handler.download_blob(request.user, file_name)
            return response
        except Exception as e:
            messages.error(request, "Internal Server Error. Please try again later.")
            return render(request, 'error_page.html', {'error_message': "Internal Server Error."})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


