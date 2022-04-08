from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as __
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib import admin
from django.conf import settings

from rest_framework import serializers


class MyUserManager(BaseUserManager):
	def create_user(self, username, email, role, password, **other_fields):
		if not email:
			raise serializers.ValidationError('enter a valid email')
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, role=role, **other_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, role, password, **other_fields):
		other_fields.setdefault('is_superuser', True)

		if other_fields.get('is_superuser') is not True:
			raise serializers.ValidationError('superuser must have is_superuser to true')

		if role != 'admin':
			raise serializers.ValidationError('superuser must have role to admin')

		return self.create_user(username, email, role, password, **other_fields)



class UserObject(models.Manager):
	def get_queryset(self):
		return super(UserObject,self).get_queryset().all()

class User(AbstractUser):

	class Roles(models.TextChoices):
		admin = 'admin', 'admin'
		staff = 'staff', 'staff'
		customer = 'customer', 'customer'

	username = models.CharField(max_length=255, unique=True)
	email = models.EmailField(max_length=255, unique=True)
	email_verified = models.BooleanField(default=False)
	first_name = models.CharField(max_length=255, null=True, blank=True)
	last_name = models.CharField(max_length=255, null=True, blank=True)
	role = models.CharField(max_length=255, choices=Roles.choices, default='customer')

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email','role']

	def __str__(self):
		return self.username

	def save(self, *args, **kwargs):
		if self.is_superuser==True:
			self.role = 'admin'
			self.is_staff=self.is_active=True
		if self.role == 'admin':
			self.is_superuser=self.is_active=self.is_staff=True
		super().save(*args, **kwargs)


	objects = MyUserManager()
	home_users = UserObject()


