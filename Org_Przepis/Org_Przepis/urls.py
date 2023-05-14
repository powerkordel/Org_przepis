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
from django.contrib import admin
from django.urls import path
from Przepisy import views
from Przepisy.views import register_view, login_view, logout_view, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('przepisy', views.przepisy, name='przepisy'),
    path('edytuj_przepis<int:pk>', views.edytuj_przepis, name='edytuj_przepis'),
    path('zapisz_przepis<int:pk>', views.zapisz_przepis, name='zapisz_przepis'),
    path('zdjecia/<str:zdjecie>', views.zdjecie),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home')
]
