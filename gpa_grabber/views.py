from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django import forms
import requests
import json

# Forms
class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=10)
    password = forms.CharField(label="Password", max_length=64)

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

    elif request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = str(request.POST.get("username"))
            password = str(request.POST.get("password"))
            login = "http://193.227.34.50/backend/api/login"
            profile = "http://193.227.34.50/backend/api/students/profile"

            data = {
                "username": username,
                "password": password
            }

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

            # Login POST request 
            conn = requests.post(login, data)
            if conn.status_code != 200:
                request.session['error'] = "Username or Password is wrong!"

                return HttpResponseRedirect(reverse("index"))

            
            parsed_data = json.loads(conn.content)

            header['Authorization'] = f"Bearer {parsed_data['body']['token']}"

            # Profile Details
            prof_conn = requests.get(profile, headers=header)
            parsed_data = json.loads(prof_conn.content)
            
            ar_name = parsed_data['body']['arabic_full_name']
            gpa = round(float(parsed_data['body']['GPA']), 2)
            email = parsed_data['body']['email']
            sitting_number = parsed_data['body']['sitting_number']

            ctx = {
                "ar_name" : ar_name,
                "gpa" : gpa,
                "email" : email,
                "sitting_number" : sitting_number,
                "gpa_found" : True
            }

            request.session['content'] = ctx

            return HttpResponseRedirect(reverse("index"))


