from django.urls import path
from . import views

#Url for endpoint1 and endpoint2
urlpatterns = [
    path('v1/wup_index>',endpoint1, name='endpoint1'),
    path('v1/wup_index/<processing_index>',endpoint2, name='endpoint2'),
]