"""
URL configuration for Org_Przepis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from Przepisy import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('przepisy', views.przepisy, name= 'przepisy'),
    path('edytuj_przepis<int:pk>', views.edytuj_przepis, name='edytuj_przepis'),
    path('usun_przepis<int:pk>', views.usun_przepis, name='usun_przepis'),
    path('dodaj_przepis', views.dodaj_przepis, name='dodaj_przepis'),
    path('zdjecia/<str:zdjecie>', views.zdjecie),
    path('static/<str:plik>', views.statyczne_pliki),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home')
]
