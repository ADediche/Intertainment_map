from django.contrib import admin

from .models import Place, Images, Coordinates


admin.site.register(Place)
admin.site.register(Images)
admin.site.register(Coordinates)