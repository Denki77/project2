from django.contrib.auth.models import User
from django.db import models

from project2.settings import MEDIA_COMPANY_IMAGE_DIR
from project2.settings import MEDIA_SPECIALITY_IMAGE_DIR


class SiteSettings(models.Model):
    key_settings = models.CharField(max_length=255)
    value_settings = models.CharField(max_length=255)


class Companies(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=64)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, default='no-image.png')
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)


class Speciality(models.Model):
    code = models.SlugField()
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR, default='no-image.png')


class Vacancies(models.Model):
    title = models.CharField(max_length=255)
    specialty = models.ForeignKey(Speciality, related_name='vacancies', on_delete=models.CASCADE)
    company = models.ForeignKey(Companies, related_name='vacancies', on_delete=models.CASCADE)
    skills = models.CharField(max_length=255)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()


class Application(models.Model):
    written_username = models.CharField(max_length=255)
    written_phone = models.CharField(max_length=255)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancies, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)
