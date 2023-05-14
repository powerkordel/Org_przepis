


from Org_Przepis import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Przepis
import os
from django.conf import settings
from django.http import HttpResponse

# Create your views here.

def przepisy(request):
    wszystkie_przepisy = Przepis.objects.all()
    dane = {
        'przepisy': wszystkie_przepisy,
    }
    return render(request, 'lista_przepisow.html', dane)

def zdjecie(request, zdjecie):
    _, rozszerzenie = os.path.splitext(zdjecie)
    sciezka = request.path
    try:
        with open(f'{settings.BASE_DIR}{sciezka}', "rb") as obrazek:
            bajty_obrazka = obrazek.read()
            return HttpResponse(bajty_obrazka, content_type=f'image/{rozszerzenie}')
    except:
        return HttpResponse([], content_type=f'image/{rozszerzenie}')


def register_view(request):
    # obsługa formularza rejestracji
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # zalogowanie nowo zarejestrowanego użytkownika
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    # obsługa formularza logowania
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            # zalogowanie użytkownika
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    # wylogowanie użytkownika
    logout(request)
    return redirect('home')



@login_required
def home(request):
    wszystkie_przepisy = Przepis.objects.all()
    dane = {
        'przepisy': wszystkie_przepisy,
    }
    return render(request, 'lista_przepisow.html', dane)

#jeszcze do ogarniecia