from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.CharField()
    student_name = models.CharField()
    authorization = models.CharField()
    gpa = models.FloatField()
    