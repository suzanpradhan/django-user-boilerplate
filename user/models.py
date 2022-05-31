from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    email = models.EmailField(_("Email Address"), unique=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=20,  null=True, blank=True)

    def __str__(self) -> str:
        return self.email
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
