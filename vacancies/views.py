from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render

from django.views import View

from vacancies.models import Speciality, Companies, Vacancies, SiteSettings


def custom_handler404(request, exception):
    return HttpResponseNotFound('<h1>Error 404</h1>Тут нет того, что вы искали!')


def custom_handler500(request):
    return HttpResponseServerError('<h1>Error 500</h1>Ой, что то сломалось... Простите, извините!')


def get_config_dict():
    title = SiteSettings.objects.filter(key_settings='site_name').first()
    menu_title = SiteSettings.objects.filter(key_settings='menu_title').first()
    return {
        'title': title.value_settings,
        'menu_title': menu_title.value_settings,
    }


class MainView(View):
    def get(self, request):
        list_of_specialty = Speciality.objects.all()
        list_of_company = Companies.objects.all()
        return render(request, 'vacancies/index.html', context={
            'base_site_config': get_config_dict(),
            'list_of_specialty': list_of_specialty,
            'list_of_company': list_of_company
        })


class VacanciesListView(View):
    def get(self, request):
        list_of_specialty = Speciality.objects.all()
        return render(request, 'vacancies/vacancies.html', context={
            'base_site_config': get_config_dict(),
            'list_of_specialty': list_of_specialty
        })


class VacancyView(View):
    def get(self, request, vacancy_id):
        data_of_vacancy = Vacancies.objects.filter(id=vacancy_id).first()
        if data_of_vacancy is None:
            raise Http404
        return render(request, 'vacancies/vacancy.html', context={
            'base_site_config': get_config_dict(),
            'data_of_vacancy': data_of_vacancy
        })


class VacanciesListBySpecializationsView(View):
    def get(self, request, specialization):
        list_of_specialty = Speciality.objects.filter(code=specialization)
        if list_of_specialty.count() == 0:
            raise Http404
        return render(request, 'vacancies/vacancies.html', context={
            'base_site_config': get_config_dict(),
            'list_of_specialty': list_of_specialty
        })


class CompaniesListView(View):
    def get(self, request):
        return render(request, 'vacancies/companies.html', context={
            'base_site_config': get_config_dict(),
        })


class CompanyView(View):
    def get(self, request, company_id):
        data_of_company = Companies.objects.filter(id=company_id).first()
        if data_of_company is None:
            raise Http404
        return render(request, 'vacancies/company.html', context={
            'base_site_config': get_config_dict(),
            'data_of_company': data_of_company
        })
