from dataclasses import dataclass


@dataclass
class WUPCalculationRequestActivating:
	status: str
	processing_id: str

@dataclass
class WUPCalculationRequestProcessing:
	status: str
	processing_id: str

@dataclass
class WUPCalculationRequestCompleted:
	status: str
	processing_id: str
