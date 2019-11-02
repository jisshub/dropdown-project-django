from django.urls import path
from .views import person_create, load_cities

urlpatterns = [
    path('', person_create, name='index'),
    path('cities', load_cities, name='cities'),
]
