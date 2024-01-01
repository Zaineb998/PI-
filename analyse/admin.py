from django.contrib import admin
from .models import *

# Register your models here.

class DataAdmin(admin.ModelAdmin):
    list_display = ('titre', 'predicted_pabel', 'sentiment', 'release_date')
    search_fields = ('titre','predicted_pabel', 'sentiment', 'uuid')
    list_filter = ('titre','sentiment', 'predicted_pabel', 'release_date')

admin.site.register(Data, DataAdmin)
