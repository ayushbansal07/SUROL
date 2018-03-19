from django.contrib import admin
from .models import Student, Professor, Registers, Course, Personal_deadline, Course_deadline, Takes
# Register your models here.
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Registers)
admin.site.register(Course)
admin.site.register(Personal_deadline)
admin.site.register(Course_deadline)
admin.site.register(Takes)
