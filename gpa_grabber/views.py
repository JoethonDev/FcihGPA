from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.http import JsonResponse
import requests
import json
from .models import Student

# Forms
class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=10, widget=forms.TextInput(attrs={"class" : "form-control", "autocomplete" : "off"}))
    password = forms.CharField(label="Password", max_length=64, widget=forms.TextInput(attrs={"class" : "form-control", "autocomplete" : "off"}))

# General Functions
def build_header(request, token=None):
    header = {
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en",
                "Authorization": "",
                "Connection": "keep-alive",
                "Host": "193.227.34.50",
                "If-None-Match": "01e9ad1e34024cdc81ed6cf87df54674",
                "Origin": "http://education.fcih.helwan.edu.eg",
                "Referer": "http://education.fcih.helwan.edu.eg/",
                "Sec-GPC": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "accept": "application/json"
            }
    if token:
        header['Authorization'] = f"Bearer {token}"
    else:
        header['Authorization'] = request.session['authorization']
    
    return header

def get_profile(header):
    profile = "http://193.227.34.50/backend/api/students/profile"

    # Profile Details
    prof_conn = requests.get(profile, headers=header)
    parsed_data = json.loads(prof_conn.content)
    
    ar_name = parsed_data['body']['arabic_full_name']
    email = parsed_data['body']['email']
    # sitting_number = parsed_data['body']['sitting_number']

    return {
                "ar_name" : ar_name,
                "email" : email,
                # "sitting_number" : sitting_number,
            }

def get_gpa(header):
    results = "http://193.227.34.50/backend/api/student/result"

    # Profile Details
    prof_conn = requests.get(results, headers=header)
    parsed_data = json.loads(prof_conn.content)
    gpa = round(float(parsed_data['body']['GPA']), 2)

    return {
                "gpa" : gpa,
                "gpa_found" : True
            }

# Create your views here.
def index(request):
    if request.method == "GET":  
        ctx = request.session.pop('content', {})
        error = request.session.pop('error', "")
        form = LoginForm()
        return render(request, 'index.html', {
            'form' : form,
            'error' : error,
            **ctx
        })

def get_results(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = str(request.POST.get("username"))
            password = str(request.POST.get("password"))
            login = "http://193.227.34.50/backend/api/login"

            data = {
                "username": username,
                "password": password
            }

            # Login POST request 
            conn = requests.post(login, data, headers={
                "origin" : "http://education.fcih.helwan.edu.eg"
            })
            if conn.status_code != 200:
                request.session['error'] = "Username or Password is wrong!"

                return HttpResponseRedirect(reverse("index"))

            parsed_data = json.loads(conn.content)
            header = build_header(request, parsed_data['body']['token'])

            ctx = {
                **get_profile(header),
                **get_gpa(header),
            }
            student = Student.objects.filter(student_id=username)
            if not student:
                Student.objects.create(student_id=username, student_name=ctx['ar_name'], authorization=header['Authorization'], gpa=ctx['gpa'])
            else:
                Student.objects.filter(student_id=username).update(authorization=header['Authorization'], gpa=ctx['gpa'])
            request.session['content'] = ctx
            request.session['authorization'] = header['Authorization']

    return HttpResponseRedirect(reverse("index"))
    
def get_grades(request):
    response = {}
    status_code = 404
    if "authorization" in request.session:
        grades_url = "http://193.227.34.50/backend/api/student/result"
        header = build_header(request)
        conn =  requests.get(grades_url, headers=header)

        response = json.loads(conn.content)
        if "body" in response:
            status_code = 200
            # Grades
            try:
                response = {
                    "grades" : [
                        {
                            "subject" : grade["course_name"],
                            "courseWork" : grade["semester_work_grade"],
                            "finalGrade" : grade["final_grade"],
                            "total" : grade["total_grade"],
                            "symbol" : grade["general_grade"]
                        }
                        for grade in response["body"]["results"]
                    ]

                }
            except Exception:
                status_code = 404
        
    return JsonResponse(response, status=status_code)