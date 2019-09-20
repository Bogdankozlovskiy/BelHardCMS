from django.urls import path

from .views import *


urlpatterns = [
    path('', vacancies_list, name='vacancies_list'),
    path('vacancy/<str:slug>/', vacancy_detail, name='vacancy_detail_url'),
]
