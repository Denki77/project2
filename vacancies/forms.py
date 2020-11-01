from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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
