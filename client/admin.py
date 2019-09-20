from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'lastname', 'state', 'skills', 'education', 'citizenship', 'city',
    )
    list_display_links = (
        'state', 'lastname'
    )


admin.site.register(Client, ClientAdmin)
