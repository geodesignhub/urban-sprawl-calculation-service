from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from dataclasses import asdict
from dacite import from_dict
from django.http import JsonResponse
import sprawl_index_generator
import uuid
from .models import WUPCalculation
from django.http import JsonResponse
from .data_definitions import WUPCalculationResult, WUPCalculationRequestActivating, WUPCalculationRequestProcessing, WUPCalculationRequestCompleted, WUPCalculationRequestRejected, WUPCalculationRequestError, WUPIndexGeneratorRequest, ErrorResponse, AlgorithmProcessingParameters
from geojson import Feature, Polygon
# Create your views here.


""" Start a WUP index calculation processing request """

@api_view(['PUT'])
def wup_index_generator(request):
    processing_parameters = request.data
    request_data = WUPIndexGeneratorRequest.from_dict(processing_parameters)
    if not request_data.is_valid():
        error_response = ErrorResponse(code=400, message="Incorrect request parameters, please review the documentation and provide full and correct data in the request")
        return JsonResponse(asdict(error_response), status=status.HTTP_400_BAD_REQUEST)

    p = Polygon(coordinates=request_data.vector_boundary['geometry']['coordinates'])
    
    if not p.is_valid:
        invalid_geometry_response = ErrorResponse(code=400, message="GeoJSON provided is not a valid Polygon, please check your vector boundary GeoJSON and resubmit")
        return JsonResponse(asdict(invalid_geometry_response), status=status.HTTP_400_BAD_REQUEST)
        
    f = Feature(geometry=p, properties={})

    w = WUPCalculation(resident_count_in_boundary = request_data.resident_count_in_boundary, employment_count_in_boundary = request_data.employment_count_in_boundary,raster_with_build_up_area = request_data.raster_with_build_up_area, raster_no_data_value = request_data.raster_no_data_value, raster_build_up_value= request_data.raster_build_up_value , vector_boundary= request_data.vector_boundary, share_of_settlement_area = request_data.share_of_settlement_area)
    w.save()
   

    algorithm_parameters = AlgorithmProcessingParameters(processing_id= str(w.id),share_of_settlement_area= request_data.share_of_settlement_area, resident_count_in_boundary=request_data.resident_count_in_boundary, employment_count_in_boundary= request_data.employment_count_in_boundary, raster_build_up_value=request_data.raster_build_up_value, raster_no_data_value= request_data.raster_no_data_value,  vector_boundary=f)
    # TODO: Make it async
    sprawl_index_generator.generate_sprawl_indices(parameters= algorithm_parameters)

    activating_response = WUPCalculationRequestActivating(status='Activating',processing_id= uuid.uuid4(),created_at= w.created_at, updated_at= w.updated_at)

    return JsonResponse(asdict(activating_response), status=200)


""" A endpoint to see results of a index calculation processing request """

@api_view(['GET'])
def index_calculation_status(request, processing_id):
    try:
        wup_calculation = WUPCalculation.objects.get(processing_id=processing_id)
    except WUPCalculation.DoesNotExist:
        error_response = ErrorResponse(code=404, message="No processing job with provided ID {processing_id} found, please check your request parameters.".format(processing_id = processing_id))
        return JsonResponse(asdict(error_response), status=status.HTTP_404_NOT_FOUND)

    if wup_calculation.status == "Activating":
        response_data = WUPCalculationRequestActivating(
            status=wup_calculation.status,
            processing_id=wup_calculation.processing_id,
            created_at=wup_calculation.created_at,
            updated_at=wup_calculation.updated_at
        )
    elif wup_calculation.status == "Processing":
        response_data = WUPCalculationRequestProcessing(
            status=wup_calculation.status,
            processing_id=wup_calculation.processing_id,
            created_at=wup_calculation.created_at,
            updated_at=wup_calculation.updated_at
        )
    elif wup_calculation.status == "Completed":
        response_data = WUPCalculationRequestCompleted(
            status=wup_calculation.status,
            processing_id=wup_calculation.processing_id,
            result=WUPCalculationResult(
                dis=wup_calculation.dis,
                lup=wup_calculation.lup,
                wup=wup_calculation.wup
            ),
            created_at=wup_calculation.created_at,
            updated_at=wup_calculation.updated_at
        )
    elif wup_calculation.status == "Rejected":
        response_data = WUPCalculationRequestRejected(
            status=wup_calculation.status,
            processing_id=wup_calculation.processing_id,
            created_at=wup_calculation.created_at,
            updated_at=wup_calculation.updated_at
        )
    else:
        response_data = WUPCalculationRequestError(
            status=wup_calculation.status,
            processing_id=wup_calculation.processing_id,
            created_at=wup_calculation.created_at,
            updated_at=wup_calculation.updated_at
        )

    return JsonResponse(asdict(response_data), status=status.HTTP_200_OK)
    

