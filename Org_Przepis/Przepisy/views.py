from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Przepis, User
import os
from Org_Przepis import settings
from .formularze import PrzepisForm

# Create your views here.


def przepisy(request):
    if (request.GET.get('przycisk_usun')):
        Przepis.delete()
    uzytkownik = User.objects.get(pk=request.user.pk)
    wszystkie_przepisy = Przepis.objects.filter(autor=uzytkownik)
    for przepis in wszystkie_przepisy:
        przepis.opis_podzielony = przepis.opis.split('\n')
        przepis.k = przepis.kategorie.all()
    dane = {
        'przepisy': wszystkie_przepisy,
    }
    return render(request, 'lista_przepisow.html', dane)


def usun_przepis(request, pk):
    if request.method == 'GET':
        przepis = Przepis.objects.get(pk=pk)
        przepis.delete()
        return redirect(reverse('przepisy'))


def dodaj_przepis(request):
    if request.method == 'POST':
        przepis = Przepis()
        przepis.autor = User.objects.get(pk=request.user.pk)
        formularz = PrzepisForm(request.POST, request.FILES, instance=przepis)
        if formularz.is_valid():
            nowy_przepis = formularz.save()
            nowy_przepis.save()
            return redirect('przepisy')
    else:
        przepis = Przepis()
        przepis.autor = User.objects.get(pk=request.user.pk)
        formularz = PrzepisForm(instance=przepis)
    dane = {
        'form': formularz,
        'tytul_formularza': 'Dodaj przepis',
        'tresc_przycisku': 'Dodaj'
    }
    return render(request, 'generyczny_formularz.html', dane)


def edytuj_przepis(request, pk):
    if request.method == 'POST':
        przepis = Przepis.objects.get(pk=pk)
        formularz = PrzepisForm(request.POST, request.FILES, instance=przepis)
        if formularz.is_valid():
            formularz.autor = User.objects.get(pk=request.user.pk)
            nowy_przepis = formularz.save()
            # nowy_przepis.autor = User.objects.get(id=request.user.id)
            nowy_przepis.save()
            return redirect('przepisy')
    else:
        przepis = Przepis.objects.get(pk=pk)
        formularz = PrzepisForm(instance=przepis)
    dane = {
        'form': formularz,
        'tytul_formularza': 'Edytuj przepis',
        'tresc_przycisku': 'Zapisz',
    }
    return render(request, 'generyczny_formularz.html', dane)

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
            redirect(reverse('home'))
    else:
        form = UserCreationForm()
    dane = {
        'form': form,
        'tytul_formularza': 'Rejestracja',
        'tresc_przycisku': 'Zarejestruj się',
    }
    return render(request, 'generyczny_formularz.html', dane)


def login_view(request):
    # obsługa formularza logowania
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            # zalogowanie użytkownika
            login(request, user)
            redirect(reverse('home'))
    else:
        form = AuthenticationForm()
    dane = {
        'form': form,
        'tytul_formularza': 'Logowanie',
        'tresc_przycisku': 'Zaloguj się',
    }
    return render(request, 'generyczny_formularz.html', dane)


def logout_view(request):
    # wylogowanie użytkownika
    logout(request)
    return redirect(reverse('home'))


def home(request):
    if request.user.is_anonymous:
        return redirect(reverse('login'))
    else:
        return redirect(reverse('przepisy'))


#jeszcze do ogarniecia