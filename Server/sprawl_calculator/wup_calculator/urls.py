from django.urls import path
from . import views

#Url for wup_index_generator and index_calculation_status
urlpatterns = [
    path('v1/wup_index',wup_index_generator, name='wup_index_generator'),
    path('v1/wup_index/<uuid:processing_id>',index_calculation_status, name='index_calculation_status'),
]