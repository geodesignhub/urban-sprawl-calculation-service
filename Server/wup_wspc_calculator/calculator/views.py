from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .wup_processing import *
# Create your views here.

@api_view(['GET'])
def calculate_wup(request):
    # Get input values from the request
    dis_value = request.GET['dis_value']
    lup_value = request.GET['lup_value']
    up_value = request.GET['up_value']
    
    # Calculate WUP
    wup_calculator = WupCalculator(up_value, dis_value, lup_value)
    wup_value = wup_calculator.calculate()
    
    # Return the result as a JSON response
    return JsonResponse({"wup": wup_value})

@api_view(['GET'])
def calculate_wspc(request):
    # Get input values from the request
    area = request.GET['area']
    resident_employee_count = request.GET['resident_employee_count']
    wup_value = request.GET['wup_value']
    
    # Calculate WSPC
    wspc_calculator = WspcCalculator(area, resident_employee_count, wup_value)
    wspc_value = wspc_calculator.calculate()
    
    # Return the result as a JSON response
    return JsonResponse({"wspc": wspc_value})