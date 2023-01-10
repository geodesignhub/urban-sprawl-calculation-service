from django.urls import path
from . import views

#Url for endpoint1 and index_calculation_status
urlpatterns = [
    path('v1/wup_index>',endpoint1, name='endpoint1'),
    path('v1/wup_index/<processing_index>',index_calculation_status, name='index_calculation_status'),
]