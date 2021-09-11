from django.contrib import admin
from django.urls import path, include
from .views import products, product


app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('<int:pk>/', products, name='category')
]
