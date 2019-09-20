from django.shortcuts import render

from .models import Vacancy



def vacancies_list(request):

    vacancies = Vacancy.objects.all()
    return render(request, 'client/index.html', context={'vacancies': vacancies})



def vacancy_detail(request, slug):

    vacancy = Vacancy.objects.get(slug__iexact=slug)
    return render(request, 'client/vacancy_detail.html', context={'vacancy': vacancy})

# Create your views here.
