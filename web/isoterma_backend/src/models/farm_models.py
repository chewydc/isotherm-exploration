from pydantic import BaseModel
from typing import List, Optional

class Location(BaseModel):
    latitude: float
    longitude: float
    address: str
    region: str

class Bounds(BaseModel):
    north: float
    south: float
    west: float
    east: float

class Sensor(BaseModel):
    id: str
    latitude: float
    longitude: float
    status: str  # "active", "warning", "error"
    temperature: Optional[float] = None

class Farm(BaseModel):
    id: str
    name: str
    location: Location
    area_hectares: float
    bounds: Bounds
    sensors: List[Sensor]
    crops: List[str]
    owner: str
    created_at: str

class FarmListResponse(BaseModel):
    success: bool
    farms: List[Farm]

class FarmDetailResponse(BaseModel):
    success: bool
    farm: Farm