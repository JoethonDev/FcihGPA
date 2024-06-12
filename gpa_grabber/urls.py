from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('results', get_results, name='results'),
    path('grades', get_grades, name='grades'),
]