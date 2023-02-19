from urban_sprawl.raster_helper.raster_downloader import download_raster
from urban_sprawl.raster_helper.raster_operations import clip_raster_with_geojson
from osgeo import gdal
from area import area
from .models import WUPCalculation

from .urban_sprawl.dis.dis_calculator import DisCalculator
from .urban_sprawl.lup.lup_calculator import LupCalculator
from .urban_sprawl.pba.pba_calculator import PbaCalculator

from .urban_sprawl.wup.wup_calculator import WupCalculator
from .urban_sprawl.wspc.wspc_calculator import WspcCalculator
from urban_sprawl.common.common import Common
from .data_definitions import AlgorithmProcessingParameters,  WUPCalculationResult
from urban_sprawl.wup_processing import (
    get_si_raster_server,
	calculate_and_save_up_server,
	calculate_and_save_wup_b_server,
	calculate_and_save_wspc_server,
    get_si_lib,    
	calculate_and_save_wud_server,
    calculate_and_save_wdis_server,    
	calculate_and_save_ud_server,
	
)

'''
The "processAlgorithm" method is a part of the QGIS Processing Framework 
and it is used to perform some action for processing a raster and a vector layer. It is renamed to generate_sprawl_incices
'''

def generate_sprawl_indices(parameters:AlgorithmProcessingParameters) -> WUPCalculationResult:
	# Initial parameters
	processing_id = parameters.processing_id
	raster_url = parameters.raster_with_build_up_area
	built_up_area = parameters.share_of_settlement_area
	geojson = parameters.vector_boundary
	resident_count_in_boundary = parameters.resident_count_in_boundary
	employment_count_in_boundary = parameters.employment_count_in_boundary
	raster_no_data_value = parameters.raster_no_data_value
	raster_build_up_value = parameters.raster_build_up_value

	w = WUPCalculation.object.get(id = processing_id)
	w.status = 'Activating'
	w.save()

	# 1.Get the downloaded file as input raster layer.
	try:
		raster_file = download_raster(raster_url)
	except Exception as e: 
		w.status = 'Error'
		w.save()
		return
	else:
		w.status = 'Processing'
		w.save()

	try:
		raster = gdal.Open(raster_file)
	except Exception as e: 
		w.status = 'Error'
		w.save()
		return
		
	# Extract spatial metadata
	# 2.Check and add the necessary fields to the vector layer, such as "Dis" and "settlement_area".
	clipped_raster_file = clip_raster_with_geojson(raster_file, geojson.feature)
	pixel_size = Common.get_pixel_size(raster)
	si_lib = get_si_lib()
	clipped_matrix, clipped_raster, result_matrix = get_si_raster_server(	
		pixel_size= pixel_size,
		raster= raster,
		clipped_raster_path=clipped_raster_file.name, 
		si_lib = si_lib 
	)
	f_area = area(geojson['geometry'])
	feature_area = float(f_area)

	
	dis_calculator = DisCalculator(result_matrix)
	dis_value = dis_calculator.calculate()
	dis_value -1.0 if dis_value == -1 else dis_value

	# 3.Run clip_raster_with_geojson() for the downloded raster and the geojson feature.
	clipped_raster_file = clip_raster_with_geojson(raster_file = raster_file, geojson_feature=geojson.feature)
	# 4.Calculate and save the DIS for each feature using the calculate_and_save_dis() method.
	# We will not calculate this step this is calculate_and_save_settlement_area in the legacy QGIS version
	# We will not calculate this step this is calculate_and_save_total_sprawl in the legacy QGIS version
	ts_value = dis_value * built_up_area
	
	# calculate_and_save_lup 
	resident_employee_count = LupCalculator.verify_lup_input(number_of_employees= resident_count_in_boundary,number_of_inhabitants = employment_count_in_boundary)

	lup_calculator = LupCalculator(built_up_area, resident_employee_count)
	lup_value = float(lup_calculator.calculate())

	# calculate_and_save_ud
	ud_value  = calculate_and_save_ud_server(lup_value = lup_value)
	wud_value = calculate_and_save_wud_server(ud_value = ud_value)
	
	# calculate_and_save percentage_of_build_up_area
	pba_calculator = PbaCalculator(built_up_area, feature_area)
	pba_value = pba_calculator.calculate()
	#calculate_and_save_up
	up_value = calculate_and_save_up_server(dis_value=dis_value, pba_value=pba_value)		
	# 5.Calculate and save the WDIC for each feature using the calculate_and_save_wdis() method.
	wdis_value = calculate_and_save_wdis_server(dis_value)	

	wup_calculator = WupCalculator(up_value = up_value, dis_value = dis_value, lup_value = lup_value)
	wup_a_value = wup_calculator.calculate()
   
	wup_b_value = calculate_and_save_wup_b_server(wup_value=wup_a_value, ssa_value=built_up_area)
	
	wspc_value = calculate_and_save_wspc_server(
        feature_area = f_area, resident_employee_count = resident_employee_count, wup_value = wup_a_value
    )
	wspc_calculator = WspcCalculator(
		area f_area, number_of_inhabitans_and_employees = resident_employee_count, weighted_urban_proliferation = wup_value)
	
	wspc_value = wspc_calculator.calculate()
	# 6.Use the calculate() method to calculate the build-up area and settlement area for each feature.
	wup_result_calculation = WUPCalculationResult(degree_of_urban_dispersion = dis_value, total_sprawl = ts_value, Ud = ud_value, Wud=wud_value, percentage_of_build_up_area = pba_value, Up = up_value, Wdis= wdis_value,  Wup_a= wup_a_value, Wup_b = wup_b_value, weighted_sprawl_per_capita = wspc_value, land_uptake_per_inhabitant = lup_value)

	# 7.Return the results as a WUPCalculationResult object.

	w.status = 'Completed'
	w.save()

	return WUPCalculationResult(degree_of_urban_dispersion = wup_result_calculation.degree_of_urban_dispersion , land_uptake_per_inhabitant = wup_result_calculation.land_uptake_per_inhabitant, weighted_urban_proliferation = wup_result_calculation.weighted_sprawl_per_capita)
