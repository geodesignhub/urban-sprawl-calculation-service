from dataclasses import dataclass
from geojson import Feature

@dataclass
class GeoJSONFeature: 
    feature: Feature