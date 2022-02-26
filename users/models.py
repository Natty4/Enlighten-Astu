from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .validators import PhoneValidator



class User(AbstractUser):
	username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
	email = models.EmailField(_('email address'), unique = True)
	
	phone_number = models.CharField(_('phone number'), max_length = 10, validators=[PhoneValidator()], unique = True)
	
	is_instructor = models.BooleanField(default=False)
	is_other = models.BooleanField(default=False)
	

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name', 'username']
	
	def __str__(self):
		return "{}".format(self.email)



class Instructor(User):

	campus = models.CharField(max_length=369, blank=True, null=True)
	profile_pic = models.ImageField(upload_to = 'profil_pics/', null=True, blank=True)
	telegram = models.CharField(max_length=369, blank=True, null=True)
	github = models.CharField(max_length=369, blank=True, null=True)
	linkedin = models.CharField(max_length=369, blank=True, null=True)

	class Meta:
		verbose_name = 'Instructor'
		verbose_name_plural = 'Instructors'

	def __str__(self):
		return f'{self.username}'

class Other(User):

	campus = models.CharField(max_length=369, blank=True, null=True)
	profile_pic = models.ImageField(upload_to = 'profil_pics/', null=True, blank=True)
	telegram = models.CharField(max_length=369, blank=True, null=True)
	github = models.CharField(max_length=369, blank=True, null=True)
	linkedin = models.CharField(max_length=369, blank=True, null=True)

	class Meta:
		verbose_name = 'Other'
		verbose_name_plural = 'Others'

	def __str__(self):
		return f'{self.username}'