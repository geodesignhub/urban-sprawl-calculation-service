from dataclasses import dataclass

@dataclass
class WUPCalculationResult:
	dis: float
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