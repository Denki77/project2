import os
import django
import datetime

os.environ["DJANGO_SETTINGS_MODULE"] = 'project2.settings'
django.setup()  # Всякие Django штуки импортим после сетапа

from vacancies.models import Speciality, Companies, Vacancies, SiteSettings
from vacancies.data import specialties, jobs, companies

if __name__ == '__main__':

    Speciality.objects.all().delete()
    Companies.objects.all().delete()
    Vacancies.objects.all().delete()
    SiteSettings.objects.all().delete()

    SiteSettings.objects.create(
        key_settings="site_name",
        value_settings="Вакансии для Junior-разработчиков"
    )

    SiteSettings.objects.create(
        key_settings="menu_title",
        value_settings="Главная"
    )

    for specialty in specialties:
        Speciality.objects.create(
            code=specialty['code'],
            title=specialty['title'],
        )

    for company in companies:
        Companies.objects.create(
            name=company['title'],
            logo='',
            employee_count=1,
        )

    for vacancy in jobs:
        Vacancies.objects.create(
            title=vacancy['title'],
            specialty=Speciality.objects.get(code=vacancy['cat']),
            company=Companies.objects.get(name=vacancy['company']),
            description=vacancy['desc'],
            salary_min=vacancy['salary_from'],
            salary_max=vacancy['salary_to'],
            published_at=datetime.date.fromisoformat(vacancy['posted']),
        )
