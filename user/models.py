from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


'''
Name	text(30)	  
Designation	text(30)	  
Department	text(30)	  
mobile_no	text(30)	  
username	text(30)	  
# Role	bool(30)	  
Type	bool(30)
'''
# class UserManager(BaseUserManager):
#     def create_user(self, mobile_no, name=None, designation=None, department=None, user_type=None, password=None):
#         """
#         Creates and saves a User with the given email, date of
#         birth and password.
#         """
#         if not mobile_no:
#             raise ValueError('Users must have an mobile number')

#         user = self.model(
#             mobile_no   = self.normalize_email(mobile_no),
#             designation = designation,
#             department  = department,
#             user_type = user_type,
#             name = name
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, mobile_no, name, designation, department, password=None, user_type='2'):
#         """
#         Creates and saves a superuser with the given mobile_no, name, designation and password

#         """
#         user = self.create_user(
#             mobile_no=mobile_no,
#             password=password,
#             name = name,
#             designation = designation,
#             department=department,
#             user_type= user_type
#         )
        
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    GENDER_CHOICES = [(0, 'Male'), (1, 'Female'), (2, 'Other')]

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name", "date_of_birth", "gender"]

    objects = UserManager()

    full_name = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)

    def __str__(self):
        return self.email

