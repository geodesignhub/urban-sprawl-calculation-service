from django.urls import path
from . import views


# URL patterns for the calculate_wup and calculate_wspc functions
urlpatterns = [
    path('calculate_wup/', views.calculate_wup, name='calculate_wup'),
    path('calculate_wspc/', views.calculate_wspc, name='calculate_wspc'),
]