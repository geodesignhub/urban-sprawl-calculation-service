from dataclasses import dataclass


@dataclass
class WUPCalculationRequestActivating:
	status: str
	processing_id: str
