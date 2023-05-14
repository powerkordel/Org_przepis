from django import forms


class PrzepisForm(forms.Form):
    nazwa = forms.CharField(label='Nazwa', max_length=100)
    opis = forms.Textarea(label='Opis')
    czas_przygotowania = forms.IntegerField(label='Czas przygotowania')
    kategoria = forms.ChoiceField(label='Kategoria')
    zdjecie = forms.ImageField(label='Zdjecie')