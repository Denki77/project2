from django.contrib import admin

from vacancies.models import Companies, Vacancies, Application, SiteSettings, Speciality


class CompaniesAdmin(admin.ModelAdmin):
    list_display = ['name', 'employee_count', 'owner']


class VacanciesAdmin(admin.ModelAdmin):
    list_display = ['title', 'specialty_name', 'company_name', 'published_at']

    def specialty_name(self, obj):
        return obj.specialty.title
    specialty_name.short_description = 'specialty'

    def company_name(self, obj):
        return obj.company.name
    company_name.short_description = 'company'


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'written_username', 'vacancy_name']

    def user_name(self, obj):
        return obj.user.username
    user_name.short_description = 'user name'

    def vacancy_name(self, obj):
        return obj.vacancy.title
    vacancy_name.short_description = 'vacancy name'



class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['title', 'code']


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['key_settings', 'value_settings']


admin.site.register(Companies, CompaniesAdmin)
admin.site.register(Vacancies, VacanciesAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
