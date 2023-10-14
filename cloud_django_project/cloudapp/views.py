from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Witaj na stronie głównej!")
def input_text(request):
    if request.method == 'POST':
        # Jeśli przesłano formularz, pobierz napis z danych wejściowych
        user_text = request.POST.get('user_text', '')  # 'user_text' to nazwa pola formularza
        return render(request, 'display_text.html', {'user_text': user_text})
    return render(request, 'input_text.html')
