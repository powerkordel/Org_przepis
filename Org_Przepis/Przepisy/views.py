from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Przepis, Kategoria, User
import os
from Org_Przepis import settings
from .formularze import PrzepisForm

# Create your views here.


def przepisy(request):
    if (request.GET.get('przycisk_usun')):
        Przepis.delete()
    wszystkie_przepisy = Przepis.objects.all()
    for przepis in wszystkie_przepisy:
        przepis.opis_podzielony = przepis.opis.split('\n')
        przepis.k = przepis.kategorie.all()
    dane = {
        'przepisy': wszystkie_przepisy,
    }
    return render(request, 'lista_przepisow.html', dane)


def edytuj_przepis(request, pk):
    if request.method == "GET":
        przepis = Przepis.objects.get(pk=pk)
        kategorie = Kategoria.objects.all()
        dane = {
            'przepis': przepis,
            'kategorie': kategorie,
        }
        return render(request, 'edytuj_przepis.html', dane)


def zapisz_przepis(request, pk):
    if request.method == 'POST':
        post = request.POST
        przepis = Przepis.objects.get(pk=pk)
        przepis.nazwa = str(post.get('nowa_nazwa'))
        przepis.opis = str(post.get('nowy_opis'))
        przepis.czas_przygotowania_w_minutach = int(post.get('nowy_czas'))
        przepis.kalorie_na_100g = float(post.get('nowe_kalorie'))
        kategoria = str(post.get('nowa_kategoria'))
        pasujace_kategorie = Kategoria.objects.filter(nazwa=kategoria)
        if len(pasujace_kategorie) > 0:
            przepis.kategoria = pasujace_kategorie[0]
        nowe_zdjecie = request.FILES.get('nowe_zdjecie')
        if nowe_zdjecie is not None:
            przepis.zdjęcie = nowe_zdjecie
        przepis.save()
        return redirect(reverse('przepisy'))


def usun_przepis(request, pk):
    if request.method == 'GET':
        przepis = Przepis.objects.get(pk=pk)
        przepis.delete()
        return redirect(reverse('przepisy'))


def dodaj_przepis(request):
    if request.method == 'POST':
        formularz = PrzepisForm(request.POST, request.FILES)
        if formularz.is_valid():
            nowy_przepis = formularz.save()
            # nowy_przepis.autor = User.objects.get(id=request.user.id)
            nowy_przepis.save()
            return redirect('przepisy')
    else:
        formularz = PrzepisForm()
    return render(request, 'dodaj_przepis.html', {'form': formularz})



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
    return render(request, 'register.html', {'form': form})


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
    return render(request, 'login.html', {'form': form})


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