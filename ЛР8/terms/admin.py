from django.contrib import admin

# Register your models here.

from .models import Tag, Termin

admin.site.register(Tag)
admin.site.register(Termin)