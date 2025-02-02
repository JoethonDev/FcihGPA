from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    search_fields = ("student_name", "student_id")

# Register your models here.
admin.site.register(Student, StudentAdmin)