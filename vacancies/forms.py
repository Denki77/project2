from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from vacancies.models import Speciality


class ApplicationForm(forms.Form):
    written_username = forms.CharField(max_length=255, label='Вас зовут')
    written_phone = forms.CharField(max_length=255, label='Ваш телефон')
    written_cover_letter = forms.CharField(label='Сопроводительное письмо', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'send'
        self.helper.add_input(Submit('submit', 'Откликнуться на вакансию'))
        self.helper.form_class = 'card mb-3 p-4'
        self.helper.label_class = 'mb-1 mt-2'


class CompanyForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)
    name = forms.CharField(max_length=255, label='Название компании')
    location = forms.CharField(max_length=64, required=False, label='Расположение компании')
    logo = forms.ImageField(required=False, label='Логотип компании')
    description = forms.CharField(label='Описание компании', required=False, widget=forms.Textarea)
    employee_count = forms.IntegerField(required=False, label='Сотрудников в  компании')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', 'Сохранить данные компании'))
        self.helper.form_class = 'card mb-3 p-4'
        self.helper.label_class = 'mb-1 mt-2'


class VacancyEditForm(forms.Form):
    specialty_names = Speciality.objects.values_list('id', 'title').all()
    id = forms.IntegerField(widget=forms.HiddenInput)
    title = forms.CharField(max_length=255, label='Название вакансии')
    specialty = forms.ChoiceField(required=False, label='Специализация', widget=forms.Select, choices=specialty_names)
    salary_min = forms.IntegerField(required=False, label='Зарплата от')
    salary_max = forms.IntegerField(required=False, label='Зарплата до')
    skills = forms.CharField(label='Требуемые навыки', required=False, widget=forms.Textarea)
    description = forms.CharField(label='Описание вакансии', required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', 'Сохранить'))
        self.helper.form_class = 'card mb-3 p-4'
        self.helper.label_class = 'mb-1 mt-2'
