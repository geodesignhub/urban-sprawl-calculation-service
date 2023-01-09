from django.urls import path
from . import views


# URL patterns for the endpoint1 and endpoint2 functions
urlpatterns = [
    path('endpoint1/', views.endpoint1, name='endpoint1'),
    path('endpoint2/', views.endpoint2, name='endpoint2'),
]