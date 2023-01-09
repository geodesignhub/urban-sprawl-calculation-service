from django.urls import path
from . import views

#Url for endpoint1 and endpoint2
urlpatterns = [
    path('endpoint1/',endpoint1, name='endpoint1'),
    path('endpoint2/',endpoint2, name='endpoint2'),
]