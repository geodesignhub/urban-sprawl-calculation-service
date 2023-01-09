from django.shortcuts import render
from rest_framework.decorators import api_view
# Create your views here.

#Endpoint1_View
@api_view(['PUT', 'GET'])
def endpoint1(request):
    raise NotImplementedError

#Endpoint2_View
@api_view(['PUT', 'GET'])
def endpoint1(request):
    raise NotImplementedError