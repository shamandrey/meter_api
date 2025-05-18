from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple, TypedDict

class MeterItem(TypedDict):
    meterID: int
    meter_type: str
    currentValue: float

class MeterResponse(TypedDict):
    getLkMeterItems: List[MeterItem]



@dataclass
class AuthData:
    token: str
    expires: datetime