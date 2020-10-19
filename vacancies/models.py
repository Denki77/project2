from django.db import models


class SiteSettings(models.Model):
    key_settings = models.CharField(max_length=255)
    value_settings = models.CharField(max_length=255)


class Companies(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=64)
    logo = models.CharField(max_length=255)
    description = models.TextField()
    employee_count = models.IntegerField()


class Speciality(models.Model):
    code = models.SlugField()
    title = models.CharField(max_length=255)
    picture = models.CharField(max_length=64)


class Vacancies(models.Model):
    title = models.CharField(max_length=255)
    specialty = models.ForeignKey(Speciality, related_name='vacancies', on_delete=models.CASCADE)
    company = models.ForeignKey(Companies, related_name='vacancies', on_delete=models.CASCADE)
    skills = models.CharField(max_length=255)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()
