from django.forms import ModelForm
from .models import Przepis


class PrzepisForm(ModelForm):
    class Meta:
        model = Przepis
        fields = ['nazwa', 'opis', 'czas_przygotowania_w_minutach', 'kategorie', 'zdjęcie', 'kalorie_na_100g']
