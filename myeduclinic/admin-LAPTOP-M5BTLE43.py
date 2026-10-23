from django.contrib import admin
from .models import Mentor, Student, Subject, Tuition
# Register your models here.
admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Tuition)