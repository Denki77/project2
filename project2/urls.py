"""project2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from vacancies.views import MainView, custom_handler404, custom_handler500, VacanciesListView, VacancyView, \
    VacanciesListBySpecializationsView, CompaniesListView, CompanyView

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', MainView.as_view()),

    path('vacancies/', VacanciesListView.as_view(), name='vacancies'),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/cat/<str:specialization>/', VacanciesListBySpecializationsView.as_view(), name='specialization'),

    path('companies/', CompaniesListView.as_view(), name='companies'),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company'),
]
