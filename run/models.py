from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import (BaseUserManager,
                                        PermissionsMixin)
from .base import BaseModel
from django.contrib.auth.models import UserManager
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class CustomUser(AbstractBaseUser,PermissionsMixin,BaseModel):

    class Meta:
        db_table = 'users'


    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=15,null=False)
    last_name  = models.CharField(max_length=15)
    is_email_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=15,unique=True,null=False)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['username','email']

class ConnectedUser(models.Model):
    class Meta:
        db_table = 'connect'
    
    username = models.CharField(max_length=15,unique=True,null=False)
    people = ArrayField(models.CharField(max_length=15),null=True)

