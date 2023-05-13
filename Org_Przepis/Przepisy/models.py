from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Kategoria(models.Model):
    class Meta:
        verbose_name_plural = 'Kategoria'
    nazwa = models.CharField(max_length=50)

    def __str__(self):
        return self.nazwa

class Przepis(models.Model):
    class Meta:
        verbose_name_plural = 'Przepis'
    nazwa = models.CharField(max_length=200)
    opis = models.TextField()
    czas_przygotowania = models.IntegerField()
    trudnosc = models.IntegerField()
    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE)
    zdjecie = models.ImageField(upload_to='zdjecia/', null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nazwa

class Skladnik(models.Model):
    class Meta:
        verbose_name_plural = 'Skladniki'
    nazwa = models.CharField(max_length=100)
    id_miary = models.ForeignKey('Miary', on_delete=models.CASCADE)

    def __str__(self):
        return self.nazwa

class Miary(models.Model):
    class Meta:
        verbose_name_plural = 'Miary'
    nazwa = models.CharField(max_length=50)

    def __str__(self):
        return self.nazwa

class PrzepisSkladnik(models.Model):
    class Meta:
        verbose_name_plural = 'PrzepisSkladnik'
    id_przepisu = models.ForeignKey(Przepis, on_delete=models.CASCADE)
    id_skladnika = models.ForeignKey(Skladnik, on_delete=models.CASCADE)
    ilosc = models.FloatField()

    def __str__(self):
        return f'{self.id_przepisu} - {self.id_skladnika}'