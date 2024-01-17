from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
import logging


def authenticate_user(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            messages.warning(request, 'Please log in to access this page.')
            return redirect('index_page')

    return wrapper
