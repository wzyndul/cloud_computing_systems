from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse

from cloud_django_project.forms import UserRegistrationForm


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            if 'login' in request.POST:
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user:
                    return redirect('success_page')
                else:
                    return HttpResponse('Invalid login credentials')

            elif 'register' in request.POST:
                form.save()  # This will create a new user
                # Redirect the user to a success page or any other appropriate action
                return redirect('success_page')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def success_page(request):
    users = User.objects.all()  # Retrieve all users
    return render(request, 'success.html', {'users': users})
