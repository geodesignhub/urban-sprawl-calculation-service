from dataclasses import dataclass


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
	result: float
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