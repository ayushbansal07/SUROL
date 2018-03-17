from django.db import models

# Create your models here.

class Student(models.Model):
	name = models.CharField(max_length=40,blank=False)
	email = models.EmailField(max_length=40,blank=False)
	dept_name = models.CharField(max_length=20,blank=False)
	password = models.CharField(max_length=20,blank=False)

class Professor(models.Model):
	name = models.CharField(max_length=40,blank=False)
	email = models.EmailField(max_length=40,blank=False)
	dept_name = models.CharField(max_length=20,blank=False)
	password = models.CharField(max_length=20,blank=False)


