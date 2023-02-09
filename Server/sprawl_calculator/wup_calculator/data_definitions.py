from dataclasses import dataclass
from datetime import datetime

@dataclass
class WUPCalculationResult:
	degree_of_urban_dispersion: float
	lup: float
	wup: float

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
class WUPIndexGeneratorRequest:
	resident_count_in_boundary: int
	employment_count_in_boundary: int
	raster_with_build_up_area: str
	raster_no_data_value: int
	vector_boundary: str

