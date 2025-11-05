"""
AI Service for trip planning and parsing
"""
from typing import Dict, Any
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def parse_trip_request(mensagem: str) -> Dict[str, Any]:
    """
    Parse a trip request message and extract travel information.
    
    Args:
        mensagem: User's travel request message
        
    Returns:
        Dictionary with parsed travel data
    """
    try:
        # TODO: Implement actual parsing logic using OpenAI
        # This is a placeholder implementation
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a travel assistant that extracts travel information from user messages. Return a JSON object with: destino, data_inicio, data_fim, viajantes, orçamento, preferencias."},
                {"role": "user", "content": mensagem}
            ],
            response_format={"type": "json_object"}
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {"error": str(e)}


def generate_trip_plan(travel_data: Any) -> Dict[str, Any]:
    """
    Generate a detailed trip plan based on travel data.
    
    Args:
        travel_data: TravelData object with trip information
        
    Returns:
        Dictionary with generated trip plan
    """
    try:
        # TODO: Implement actual trip plan generation using OpenAI
        # This is a placeholder implementation
        travel_dict = travel_data.dict() if hasattr(travel_data, 'dict') else travel_data
        
        prompt = f"""Generate a detailed trip plan for:
        Destination: {travel_dict.get('destino', 'Unknown')}
        Start Date: {travel_dict.get('data_inicio', 'Unknown')}
        End Date: {travel_dict.get('data_fim', 'Unknown')}
        Travelers: {travel_dict.get('viajantes', 'Unknown')}
        Budget: {travel_dict.get('orçamento', 'Unknown')}
        Preferences: {travel_dict.get('preferencias', 'None')}
        
        Return a JSON object with daily itinerary."""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a travel planning assistant. Create detailed daily itineraries with activities, restaurants, and recommendations."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {"error": str(e)}

