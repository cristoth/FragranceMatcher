from django.contrib import admin
from .models import Fragrance, Perfume, Perfume_Fragrance

# Register your models here.
admin.site.register(Fragrance)
admin.site.register(Perfume)
admin.site.register(Perfume_Fragrance)