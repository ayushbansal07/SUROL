from django.db import models
from datetime import date
from django.utils import timezone

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

class Course(models.Model):
	name = models.CharField(max_length=40,blank=False)
	dept_name = models.CharField(max_length=20,blank=False)
	def __str__(self):
		return str(self.id) + " : " + str(self.name)

class Takes(models.Model):
	professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Registers(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	course = models.ForeignKey(Course,on_delete = models.CASCADE)

class Course_deadline(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	name = models.CharField(max_length=100,blank=False)
	comments = models.CharField(max_length=500,blank=False)
	date = models.DateTimeField(default=timezone.now)

class Personal_deadline(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	name = models.CharField(max_length=100,blank=False)
	date = models.DateTimeField(default=timezone.now)
	comments = models.CharField(max_length=500,blank=False)
