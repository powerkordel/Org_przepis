from django.db import models
from django.contrib.auth.models import User


class Kategoria(models.Model):
    class Meta:
        verbose_name_plural = 'Kategorie'
    nazwa = models.CharField(max_length=50)
    def __str__(self):
        return self.nazwa


class Przepis(models.Model):
    class Meta:
        verbose_name_plural = 'Przepisy'
    nazwa = models.CharField(max_length=200)
    opis = models.TextField()
    czas_przygotowania_w_minutach = models.IntegerField()
    kategorie = models.ManyToManyField(Kategoria)
    zdjęcie = models.ImageField(upload_to='zdjecia/', null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default='')
    kalorie_na_100g = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.nazwa


class Skladnik(models.Model):
    class Meta:
        verbose_name_plural = 'Skladniki'
    nazwa = models.CharField(max_length=100)
    zdjęcie_składnika = models.ImageField(upload_to='zdjecia_sklad/', null=True, blank=True)
    kalorie_na_100g = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.nazwa


class Miary(models.Model):
    class Meta:
        verbose_name_plural = 'Miary_Ilośi'
    nazwa = models.CharField(max_length=50)
    skrót = models.CharField(max_length=10, null=True, blank=True)
    def __str__(self):
        return self.nazwa


class PrzepisSkladnik(models.Model):
    class Meta:
        verbose_name_plural = 'Przepisy_Skladnik'
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE)
    składnik = models.ForeignKey(Skladnik, on_delete=models.CASCADE)
    ilość = models.FloatField()
    miara = models.ForeignKey('Miary', on_delete=models.CASCADE, null=True, default='')
    def __str__(self):
        return f'{self.przepis} - {self.składnik}'
