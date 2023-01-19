from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import WUPCalculation
from django.http import JsonResponse
from rest_framework import status
# Create your views here.

#Endpoint1_View
@api_view(['PUT', 'GET'])
def wup_index_generator(request):
    raise NotImplementedError

#Endpoint2_View
@api_view(['GET'])
def index_calculation_status(request, processing_id):
    try:
        wup_calculation = WUPCalculation.objects.get(processing_id=processing_id)
    except WUPCalculation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if wup_calculation.status == "Completed":
        data = WUPCalculation.values()
        return JsonResponse(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_202_ACCEPTED)