from django.contrib import admin
from .models import Kategoria
from .models import Przepis
from .models import Miary
from .models import PrzepisSkladnik
from .models import Skladnik
# Register your models here.
admin.site.register(Kategoria)
admin.site.register(Przepis)
admin.site.register(Miary)
admin.site.register(PrzepisSkladnik)
admin.site.register(Skladnik)