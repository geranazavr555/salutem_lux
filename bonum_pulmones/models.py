from django.db import models
from django.contrib.auth.models import User as _User


class User(models.Model):

    auth_user = models.OneToOneField(_User, primary_key=True)

    @property
    def first_name(self):
        return self.auth_user.first_name

    @property
    def last_name(self):
        return self.auth_user.last_name

    @property
    def email(self):
        return self.auth_user.email


class MedicalData(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='measurements')
    filename = models.CharField(max_length=255, primary_key=True)
    date = models.DateField(auto_now_add=True)
    result = models.FloatField(null=True)
