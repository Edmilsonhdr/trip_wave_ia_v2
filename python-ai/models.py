"""
Pydantic models for the TripWave AI API
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ParseInput(BaseModel):
    """Input model for parsing trip requests"""
    mensagem: str


class TravelData(BaseModel):
    """Model for travel data"""
    destino: str
    data_inicio: str
    data_fim: str
    viajantes: Optional[int] = None
    orçamento: Optional[float] = None
    preferencias: Optional[str] = None


class SaveRoteiroInput(BaseModel):
    """Input model for saving a roteiro (itinerary)"""
    roteiro: Dict[str, Any]
    travel_data: TravelData
    user_id: Optional[str] = None

