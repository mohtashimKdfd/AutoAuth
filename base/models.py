from django.db import models
from django.utils.translation import gettext_lazy as gl
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin # mixin for models to add feilds that are specific for objects
from django.contrib.auth.models import BaseUserManager


# Create your models here.



class CustomAccountManager(BaseUserManager):
    def create_superuser(self,email,user_name,first_name,password,**other_feilds):
        other_feilds.setdefault('is_staff',True)
        other_feilds.setdefault('is_superuser',True)
        other_feilds.setdefault('is_Active',True)

        if other_feilds.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True'
            )
        if other_feilds.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True'
            )
        return self.create_user(email,user_name,first_name,password,**other_feilds)
    
    def create_user(self,email,user_name,first_name,password,**other_feilds):
        if not email:
            raise ValueError(gl("You must provide an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email,user_name=user_name,first_name=first_name,**other_feilds)

        user.set_password(password)
        user.save()

        return user


class NewUser(AbstractBaseUser,PermissionsMixin) :
    email = models.EmailField(gl('email address'), unique=True)
    user_name = models.CharField(max_length=150,unique=True)
    first_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now())
    about = models.TextField(gl('about'),max_length=500,blank=True)
    is_staff = models.BooleanField(default=False)
    is_Active = models.BooleanField(default=False)

    objects = CustomAccountManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','first_name']

    def __str__(self):
        return self.user_name