from django.db import models

# Create your models here.
class Mentor(models.Model) :
    mentorid = models.CharField(max_length=10, primary_key=True)
    mentorname = models.CharField(max_length=100)
    mentorcourse = models.CharField(max_length=5)
    mentorphonenum = models.CharField(max_length=20)

class Student (models.Model) :
    studentid = models.CharField(max_length=15, primary_key=True)
    mentorid = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    studentname = models.CharField(max_length=100)
    studentcourse = models.CharField(max_length=5)
    studentphonenum = models.CharField(max_length=20)

class Subject(models.Model) :
    subjectcode = models.CharField(max_length=10, primary_key=True)
    subjectname = models.CharField(max_length=100)

class Tuition (models.Model) :
    tuitioncode = models.CharField(max_length=5, primary_key=True)
    studentid = models.ForeignKey(Student, on_delete=models.CASCADE)
    mentorid = models.ForeignKey(Mentor, on_delete= models.CASCADE)
    subjectcode = models.ForeignKey(Subject, on_delete= models.CASCADE)
    tuitionmeet = models.TextField(max_length=200)
    tuitiondate = models.DateField()
    tuitionduration = models.IntegerField()
    description = models.TextField(max_length=1000)
