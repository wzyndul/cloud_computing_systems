from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from cloud_django_project.forms import UserRegistrationForm, UserLoginForm
from cloudapp import blob_handler
from cloudapp.models import UserActivityLog
from cloudapp.utils import authenticate_user


def index_page(request):
    return render(request, 'index.html')


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
                UserActivityLog.objects.create(username=user, activity='register')
                return redirect('index_page')
            else:
                messages.warning(request, 'Unsuccessful registration. Invalid information.')

        except ValidationError:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
        except IntegrityError:
            messages.error(request, 'Unsuccessful registration. Username already exists.')
        except Exception:
            return render(request, 'error_page.html', {'error_message': "Internal Server Error.", 'status': 500})

    form = UserRegistrationForm()
    return render(request, 'register.html', {'register_form': form})


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
                    UserActivityLog.objects.create(username=user, activity='login')
                    return redirect('index_page')
                else:
                    messages.warning(request, "Invalid username or password.")
            else:
                messages.warning(request, "Invalid username or password.")

        except KeyError:
            messages.error(request, "Missing username or password.")
        except ValidationError:
            messages.error(request, "Invalid login form data.")
        except Exception:
            return render(request, 'error_page.html', {'error_message': "Internal Server Error.", 'status': 500})

    elif request.method == 'GET':
        if request.user.is_authenticated:
            messages.success(request,
                             f"You are already logged in as {request.user.username}.")
            return redirect('index_page')

    form = UserLoginForm()
    return render(request, 'login.html', {'login_form': form})


def logout_user(request):
    try:
        if request.user.is_authenticated:
            UserActivityLog.objects.create(username=request.user, activity='logout')
            logout(request)
            messages.info(request, "You have successfully logged out.")
            return redirect('index_page')
        else:
            raise PermissionDenied("You are not logged in.")

    except AttributeError:
        messages.error(request, "User not found.")
        return redirect('login_user')
    except PermissionDenied:
        messages.error(request, "You are not logged in.")
        return redirect('login_user')
    except Exception:
        return render(request, 'error_page.html', {'error_message': "Internal Server Error.", 'status': 500})


@authenticate_user
def storage(request):
    if request.method == 'GET':
        try:
            blobs = blob_handler.list_blobs_with_properties(request.user)
            return render(request, 'storage.html', {'blobs': blobs})

        except AttributeError:
            messages.error(request, "User not found.")
            return redirect('login_user')
        except Exception:
            return render(request, 'error_page.html', {'error_message': "Internal Server Error.", 'status': 500})

    elif request.method == 'POST':
        try:
            uploaded_files = request.FILES.getlist('files')
            if not uploaded_files:
                raise ValueError("No files uploaded.")

            blob_handler.parallel_upload_blob(request.user, uploaded_files)
            messages.success(request, f'{len(uploaded_files)} file(s) uploaded successfully.')
            return redirect('storage')

        except ValueError:
            messages.error(request, "Invalid file(s) selected.")
            return redirect('storage')
        except AttributeError:
            messages.error(request, "User not found.")
            return redirect('login_user')
        except Exception:
            return render(request, 'error_page.html', {'error_message': "Internal Server Error.", 'status': 500})

    return render(request, 'storage.html')


@authenticate_user
def change_version(request):
    if request.method == 'POST':
        try:
            file_name = request.POST.get('file_name')
            version = request.POST.get('version_id')
            if not file_name or not version:
                raise ValueError("Missing file name or version ID.")

            blob_handler.change_blob_version(request.user, file_name, version)
            return redirect('storage')

        except ValueError:
            messages.error(request, "Invalid file name or version ID.")
            return redirect('storage')
        except AttributeError:
            messages.error(request, "User not found.")
            return redirect('login_user')
        except Exception:
            return render(request, 'error_page.html', {'error_message': "Internal Server Error.", 'status': 500})

    return render(request, 'error_page.html', {'error_message': "Invalid request method.", 'status': 405})


@authenticate_user
def download_file(request):
    if request.method == 'GET':
        file_name = request.GET.get('file_name')
        try:
            if not file_name:
                raise ValueError("Missing file name.")

            response = blob_handler.download_blob(request.user, file_name)
            return response

        except ValueError:
            messages.error(request, "Invalid file name.")
            return redirect('storage')
        except AttributeError:
            messages.error(request, "User not found.")
            return redirect('login_user')
        except Exception:
            return render(request, 'error_page.html', {'error_message': "Internal Server Error.", 'status': 500})

    return render(request, 'error_page.html', {'error_message': "Invalid request method.", 'status': 405})


@authenticate_user
def delete_file(request):
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        try:
            if not file_name:
                raise ValueError("Missing file name.")

            blob_handler.delete_blob(request.user, file_name)
            return redirect('storage')

        except ValueError:
            messages.error(request, "Invalid file name.")
            return redirect('storage')
        except AttributeError:
            messages.error(request, "User not found.")
            return redirect('login_user')
        except Exception:
            return render(request, 'error_page.html', {'error_message': "Internal Server Error.", 'status': 500})

    return render(request, 'error_page.html', {'error_message': "Invalid request method.", 'status': 405})
