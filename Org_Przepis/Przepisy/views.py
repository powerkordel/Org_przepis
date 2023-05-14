from django.shortcuts import render
from django.views import View
from django.template import loader
from django.http import HttpResponse
from .models import Przepis
import os
from Org_Przepis import settings

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
