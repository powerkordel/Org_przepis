from django.shortcuts import render
from django.views import View
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Przepis, Kategoria
import os
from Org_Przepis import settings

# Create your views here.

def przepisy(request):
    if (request.GET.get('przycisk_usun')):
        Przepis.delete()
    wszystkie_przepisy = Przepis.objects.all()
    for przepis in wszystkie_przepisy:
        przepis.opis_podzielony = przepis.opis.split('\n')
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
        przepis = Przepis.objects.get(pk=pk)
        przepis.nazwa = str(request.POST.get('nowa_nazwa'))
        przepis.opis = str(request.POST.get('nowy_opis'))
        przepis.czas_przygotowania = int(request.POST.get('nowy_czas'))
        kategoria = str(request.POST.get('nowa_kategoria'))
        pasujace_kategorie = Kategoria.objects.filter(nazwa=kategoria)
        if len(pasujace_kategorie) > 0:
            przepis.kategoria = pasujace_kategorie[0]
        zdjecie = request.FILES.get('nowe_zdjecie')
        if zdjecie is not None:
            przepis.zdjecie = zdjecie
        przepis.save()
        return redirect(reverse('przepisy'))


def zdjecie(request, zdjecie):
    _, rozszerzenie = os.path.splitext(zdjecie)
    sciezka = request.path
    try:
        with open(f'{settings.BASE_DIR}{sciezka}', "rb") as obrazek:
            bajty_obrazka = obrazek.read()
            return HttpResponse(bajty_obrazka, content_type=f'image/{rozszerzenie}')
    except:
        return HttpResponse([], content_type=f'image/{rozszerzenie}')
