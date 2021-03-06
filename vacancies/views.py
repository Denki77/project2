from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404, HttpResponse
from django.shortcuts import render, redirect

from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

from vacancies.forms import ApplicationForm, CompanyForm, VacancyEditForm
from vacancies.models import Speciality, Companies, Vacancies, SiteSettings, Application


def custom_handler404(request, exception):
    return HttpResponseNotFound('<h1>Error 404</h1>Тут нет того, что вы искали!')


def custom_handler500(request):
    return HttpResponseServerError('<h1>Error 500</h1>Ой, что то сломалось... Простите, извините!')


def get_config_dict():
    title = SiteSettings.objects.filter(key_settings='site_name').first()
    menu_title = SiteSettings.objects.filter(key_settings='menu_title').first()
    user = User
    return {
        'title': title.value_settings,
        'menu_title': menu_title.value_settings,
        'is_authenticated': user.is_authenticated,
        'user_name': user.get_username,
    }


class MainView(View):
    def get(self, request):
        list_of_specialty = Speciality.objects.all()
        list_of_company = Companies.objects.all()
        return render(request, 'vacancies/index.html', context={
            'base_site_config': get_config_dict(),
            'list_of_specialty': list_of_specialty,
            'list_of_company': list_of_company,
        })


class VacanciesListView(View):
    def get(self, request):
        list_of_specialty = Speciality.objects.all()
        return render(request, 'vacancies/vacancies.html', context={
            'base_site_config': get_config_dict(),
            'list_of_specialty': list_of_specialty,
        })


class VacancyView(View):

    def get_vacancy_data(self, vacancy_id):
        return Vacancies.objects.filter(id=vacancy_id).first()

    def get(self, request, vacancy_id):
        data_of_vacancy = self.get_vacancy_data(vacancy_id)
        application_form = ApplicationForm()
        if data_of_vacancy is None:
            raise Http404
        return render(request, 'vacancies/vacancy.html', context={
            'base_site_config': get_config_dict(),
            'data_of_vacancy': data_of_vacancy,
            'form': application_form
        })


class VacancyApplicationView(View):
    def post(self, request, vacancy_id):

        if not request.user.is_authenticated:
            return redirect('/login')

        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            data_for_save = application_form.cleaned_data
            data_for_save['vacancy'] = Vacancies.objects.get(id=vacancy_id)
            data_for_save['user'] = User.objects.get(id=request.user.id)
            Application(**data_for_save).save()
            return redirect('/success')
        else:
            application_form.add_error('written_username', 'Use YYYY/MM/DD format')


class MyCompanyView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login')

        my_company_exist = False

        data_about_company = {
            'name': '0',
            'location': '',
            'logo': 'no-image.png',
            'description': '',
            'employee_count': 0
        }

        list_of_company = Companies.objects.filter(owner_id=request.user.id)
        if list_of_company.count() > 0:
            data_about_company = list_of_company.first()
            my_company_exist = True
        elif "createNewCompany" in request.GET.keys():
            Companies.objects.create(
                name='',
                location=' ',
                logo='no-image.png',
                description='',
                employee_count=1,
                owner=User.objects.get(id=request.user.id),
            )
            data_about_company = Companies.objects.filter(owner_id=request.user.id).first()
            my_company_exist = True

        context = {
            'base_site_config': get_config_dict(),
            'data_about_company': data_about_company,
            'myCompanyExist': my_company_exist,
        }

        if my_company_exist:
            context['form'] = CompanyForm({
                'id': data_about_company.id,
                'name': data_about_company.name,
                'location': data_about_company.location,
                'logo': data_about_company.logo,
                'description': data_about_company.description,
                'employee_count': data_about_company.employee_count
            })

        return render(request, 'vacancies/mycompany.html', context=context)

    def post(self, request):

        if not request.user.is_authenticated:
            return redirect('/login')

        company_form = CompanyForm(request.POST, request.FILES)
        print(company_form['location'])
        if company_form.is_valid():
            data_for_save = company_form.cleaned_data
            if data_for_save['logo'] is None:
                data_for_save['logo'] = Companies.objects.get(id=data_for_save['id']).logo
            print(data_for_save['logo'])
            data_for_save['owner'] = User.objects.get(id=request.user.id)
            Companies(**data_for_save).save()

        return redirect('my_company')


class MyCompanyVacanciesListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login')

        data_of_my_company = Companies.objects.filter(owner_id=request.user.id)
        if data_of_my_company.count() == 0:
            return redirect('my_company')

        return render(request, 'vacancies/vacancy-list.html', context={
            'base_site_config': get_config_dict(),
            'data_of_my_company': data_of_my_company.first(),
        })


class MyCompanyVacancyEditView(View):
    def get(self, request, vacancy_id):
        if not request.user.is_authenticated:
            return redirect('/login')

        if vacancy_id == 0:
            Vacancies.objects.create(
                title='Новая вакансия',
                specialty=Speciality.objects.filter().first(),
                salary_min=0,
                salary_max=0,
                description='',
                skills='',
                company=Companies.objects.filter(owner_id=request.user.id).first(),
            )
            vacancy_id = Vacancies.objects.filter(
                company=Companies.objects.filter(
                    owner_id=request.user.id).first()).last().id

        data_of_one_vacancy = Vacancies.objects.filter(id=vacancy_id)
        if data_of_one_vacancy.count() == 0:
            return redirect('my_company_vacancies')

        data_of_one_vacancy_first = data_of_one_vacancy.first()

        vacancy_form = VacancyEditForm({
            'id': data_of_one_vacancy_first.id,
            'title': data_of_one_vacancy_first.title,
            'specialty': data_of_one_vacancy_first.specialty.id,
            'salary_min': data_of_one_vacancy_first.salary_min,
            'salary_max': data_of_one_vacancy_first.salary_max,
            'skills': data_of_one_vacancy_first.skills,
            'description': data_of_one_vacancy_first.description,
        })

        return render(request, 'vacancies/vacancy-edit.html', context={
            'base_site_config': get_config_dict(),
            'data_of_one_vacancy': data_of_one_vacancy_first,
            'form': vacancy_form,
        })

    def post(self, request, vacancy_id):

        if not request.user.is_authenticated:
            return redirect('/login')

        data_of_my_company = Companies.objects.filter(owner_id=request.user.id)
        if data_of_my_company.count() == 0:
            return redirect('my_company')

        vacancy_form = VacancyEditForm(request.POST)
        if vacancy_form.is_valid():
            data_for_save = vacancy_form.cleaned_data
            data_for_save['company'] = data_of_my_company.first()
            data_for_save['specialty'] = Speciality.objects.get(id=data_for_save['specialty'])

            Vacancies(**data_for_save).save()

            if vacancy_id == 0:
                vacancy_id = data_for_save['id']

        return redirect('my_company_vacancy', vacancy_id)


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
        list_of_company = Companies.objects.all()
        return render(request, 'vacancies/companies.html', context={
            'base_site_config': get_config_dict(),
            'list_of_company': list_of_company,
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


class MySignupView(CreateView):
    extra_context = {
        'base_site_config': get_config_dict(),
    }
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'vacancies/register.html'


class MyLoginView(LoginView):
    extra_context = {
        'base_site_config': get_config_dict(),
    }
    redirect_authenticated_user = True
    template_name = 'vacancies/login.html'


class SuccessView(View):
    def get(self, request):
        return HttpResponse("Успешно!")


class ErrorView(View):
    def get(self, request):
        return HttpResponse("Что-то пошло не так(((!")
