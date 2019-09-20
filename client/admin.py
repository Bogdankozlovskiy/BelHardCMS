from django.contrib import admin
from .models import Vacancy

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


admin.site.register(Vacancy, VacancyAdmin)

# Register your models here.
