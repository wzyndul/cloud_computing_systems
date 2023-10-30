from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    if request.method == 'POST':
        # Jeśli przesłano formularz, pobierz napis z danych wejściowych
        username = request.POST["username"]
        password = request.POST["password"]
        print(username)
        print(password)

        return render(request, 'display_text.html')
    return render(request, 'input_text.html')
