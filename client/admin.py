from django.contrib import admin
from .models import Vacancy
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'lastname', 'state', 'skills', 'education', 'citizenship', 'city',
    )
    list_display_links = (
        'state', 'lastname'
    )




class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'state', 'organization', 'slug', 'address', 'employment', 'description',
        'skills', 'requirements', 'duties', 'conditions',
    )
    list_display_links = (
        'state', 'organization', 'description',
    )
    search_fields = (
        'state', 'organization', 'description',
    )


admin.site.register(Client, ClientAdmin)
admin.site.register(Vacancy, VacancyAdmin)

# Register your models here.
