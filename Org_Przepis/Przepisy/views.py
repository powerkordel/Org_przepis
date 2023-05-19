from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse, HttpRequest
from .models import Przepis, User, PrzepisSkladnik, Kategoria, Skladnik
import os
from Org_Przepis import settings
from .formularze import PrzepisForm

# Create your views here.


def przepisy(request):
    if request.GET.get('przycisk_usun'):
        Przepis.delete()
    uzytkownik = User.objects.get(pk=request.user.pk)
    wszystkie_przepisy = Przepis.objects.filter(autor=uzytkownik)
    kategoria = '*'
    skladnik = '*'
    slowo_klucz = ''
    if request.method == 'POST':
        filtrowane_przepisy = []
        post = request.POST
        kategoria = post.get('kategoria')
        skladnik = post.get('skladnik')
        slowo_klucz = post.get('slowo_klucz')
        for p in wszystkie_przepisy:
            dodac = True
            if kategoria is not '*':
                kategorie = p.kategorie.all()
                ma_kategorie = False
                for k in kategorie:
                    ma_kategorie |= kategoria == k.nazwa
                dodac = ma_kategorie
            if skladnik is not '*':
                s = Skladnik.objects.get(nazwa=skladnik)
                ps = PrzepisSkladnik.objects.filter(przepis=p, składnik=s)
                if len(ps) == 0:
                    dodac = False
            if slowo_klucz is not '':
                pasuje = False
                pasuje |= slowo_klucz.lower() in p.nazwa.lower()
                pasuje |= slowo_klucz.lower() in p.opis.lower()
                dodac = pasuje
            if dodac:
                filtrowane_przepisy.append(p)
        wszystkie_przepisy = filtrowane_przepisy

    for przepis in wszystkie_przepisy:
        przepis.opis_podzielony = przepis.opis.split('\n')
        przepis.wszystkie_kategorie = przepis.kategorie.all()
        przepis.wszystkie_skladniki = []
        for przepisSkladnik in PrzepisSkladnik.objects.filter(przepis=przepis):
                przepis.wszystkie_skladniki.append(przepisSkladnik)

    kategorie = Kategoria.objects.all()
    skladniki = Skladnik.objects.all()
    dane = {
        'przepisy': wszystkie_przepisy,
        'kategorie': kategorie,
        'skladniki': skladniki,
        'kategoria': kategoria,
        'skladnik': skladnik,
        'slowo_klucz': slowo_klucz,
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
        'tytul_strony': 'Dodaj przepis',
        'tresc_przycisku': 'Dodaj',
        'id_formularza': 'formularz_dodaj_przepis',
    }
    return render(request, 'generyczny_formularz.html', dane)


def edytuj_przepis(request, pk):
    if request.method == 'POST':
        przepis = Przepis.objects.get(pk=pk)
        formularz = PrzepisForm(request.POST, request.FILES, instance=przepis)
        if formularz.is_valid():
            formularz.autor = User.objects.get(pk=request.user.pk)
            nowy_przepis = formularz.save()
            nowy_przepis.save()
            return redirect('przepisy')
    else:
        przepis = Przepis.objects.get(pk=pk)
        formularz = PrzepisForm(instance=przepis)
    dane = {
        'form': formularz,
        'tytul_strony': 'Edytuj przepis',
        'tresc_przycisku': 'Zapisz',
        'id_formularza': 'formularz_edytuj_przepis',
    }
    return render(request, 'generyczny_formularz.html', dane)


def zdjecie(request: HttpRequest, zdjecie: str) -> HttpResponse:
    if request.user.is_anonymous:
        odpowiedz = HttpResponse()
        odpowiedz.status_code = 403
    else:
        _, rozszerzenie = os.path.splitext(zdjecie)
        sciezka = request.path
        odpowiedz = zwroc_zdjecie(sciezka, rozszerzenie)
    return odpowiedz


def statyczne_pliki(request: HttpRequest, plik: str) -> HttpResponse:
    _, rozszerzenie = os.path.splitext(plik)
    sciezka = request.path
    if rozszerzenie == 'jpeg' or rozszerzenie == 'jpg' or rozszerzenie == 'png':
        odpowiedz = zwroc_zdjecie(sciezka, rozszerzenie)
    else:
        odpowiedz = HttpResponse()
        odpowiedz.status_code = 404
    return odpowiedz


def zwroc_zdjecie(sciezka: str, rozszerzenie: str) -> HttpResponse:
    try:
        with open(f'{settings.BASE_DIR}{sciezka}', "rb") as obrazek:
            bajty_obrazka = obrazek.read()
            odpowiedz = HttpResponse(bajty_obrazka, content_type=f'image/{rozszerzenie}')
            odpowiedz.status_code = 200
    except FileNotFoundError:
        odpowiedz = HttpResponse()
        odpowiedz.status_code = 404
    return odpowiedz

def register_view(request):
    # obsługa formularza rejestracji
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # zalogowanie nowo zarejestrowanego użytkownika
            login(request, user)
            return redirect(reverse('home'))
    else:
        form = UserCreationForm()
    dane = {
        'form': form,
        'tytul_formularza': 'Rejestracja',
        'tresc_przycisku': 'Zarejestruj się',
        'id_formularza': 'formularz_rejestracja',
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
            return redirect(reverse('home'))
    else:
        form = AuthenticationForm()
    dane = {
        'form': form,
        'tytul_formularza': 'Logowanie',
        'tresc_przycisku': 'Zaloguj się',
        'id_formularza': 'formularz_logowanie',
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


