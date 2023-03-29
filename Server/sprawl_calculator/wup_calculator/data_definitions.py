from dataclasses import dataclass
from datetime import datetime
from geojson import Feature


@dataclass
class WUPCalculationResult:
	weighted_sprawl_per_capita: float
	degree_of_urban_dispersion: float
	land_uptake_per_inhabitant: float

@dataclass
class WUPCalculationResultFull:
	urban_dispersion: float
	weighted_urban_dispersion: float
	percentage_of_build_up_area: float
	total_sprawl: float
	degree_of_urban_permeation: float
	weighted_degree_of_urban_dispersion: float
	weighted_urban_proliferation_a: float
	weighted_urban_proliferation_b: float
	weighted_sprawl_per_capita: float
	degree_of_urban_dispersion: float
	land_uptake_per_inhabitant: float

@dataclass
class WUPCalculationRequestActivating:
	status: str
	processing_id: str
	created_at: datetime
	updated_at: datetime

@dataclass
class WUPCalculationRequestProcessing:
	status: str
	processing_id: str
	created_at: datetime
	updated_at: datetime

@dataclass
class WUPCalculationRequestCompleted:
	status: str
	processing_id: str
	result: WUPCalculationResult
	created_at: datetime
	updated_at: datetime
	
@dataclass
class WUPCalculationRequestRejected:
	status: str
	processing_id: str
	created_at: datetime
	updated_at: datetime

@dataclass
class WUPCalculationRequestError:
	status: str
	processing_id: str
	created_at: datetime
	updated_at: datetime

@dataclass
class ErrorResponse: 
	code: int
	message: str


@dataclass
class GeoJSONFeature: 
    feature: Feature

@dataclass
class WUPIndexGeneratorRequest:
	resident_count_in_boundary: int
	employment_count_in_boundary: int
	share_of_settlement_area:float
	raster_with_build_up_area: str
	raster_no_data_value: int
	raster_build_up_value: int
	vector_boundary: GeoJSONFeature

@dataclass
class AlgorithmProcessingParameters:
	processing_id:str
	share_of_settlement_area: float
	resident_count_in_boundary: int
	employment_count_in_boundary: int
	raster_with_build_up_area: str
	raster_no_data_value: int
	raster_build_up_value: int
	vector_boundary: dict
	
