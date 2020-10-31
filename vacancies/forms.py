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
        #self.helper.field_class = 'col-lg-8'
