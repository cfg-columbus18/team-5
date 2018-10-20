from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    language_name = models.CharField(max_length=50)

    def __str__(self):
        return self.language_name

class SponsorComponent(models.Model):
    sponsor_component = models.CharField(max_length=50)

    def __str__(self):
        return self.sponsor_component

class CommunicationPlatform(models.Model):
    communication_platform = models.CharField(max_length=50)

    def __str__(self):
        return self.communication_platform

class Profile(models.Model):
    # profile -> user ~foreignkey
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    province_state_region = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    timezone = models.CharField(max_length=50)
    communication_platforms = models.ManyToManyField(CommunicationPlatform)
    sponsor_stage = models.CharField(max_length=50)
    languages = models.ManyToManyField(Language)
    sponsor_components = models.ManyToManyField(SponsorComponent)
    faith = models.CharField(max_length=50)
    sponsor_type = models.CharField(max_length=50)
    refugee_region = models.CharField(max_length=50)
