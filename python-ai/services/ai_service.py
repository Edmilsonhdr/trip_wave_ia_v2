"""
AI Service for trip planning and parsing
"""
from typing import Dict, Any
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables - try to load from .env in the project root
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)
# Also try loading from current directory
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")

# Initialize client - support both OpenAI and Groq
if api_key and api_key.startswith("gsk_"):
    # Groq API key detected
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
elif api_key:
    # OpenAI API key
    client = OpenAI(api_key=api_key)
else:
    # No API key found
    client = None


def parse_trip_request(mensagem: str) -> Dict[str, Any]:
    """
    Parse a trip request message and extract travel information.
    
    Args:
        mensagem: User's travel request message
        
    Returns:
        Dictionary with parsed travel data
    """
    if not client:
        return {"error": "API key not configured. Please set OPENAI_API_KEY or GROQ_API_KEY in your .env file"}
    
    try:
        # Use appropriate model based on API provider
        # Groq: llama-3.3-70b-versatile (replaces deprecated llama-3.1-70b-versatile)
        model = "llama-3.3-70b-versatile" if api_key and api_key.startswith("gsk_") else "gpt-4"
        
        response = client.chat.completions.create(
            model=model,
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
        error_msg = str(e)
        if "invalid_api_key" in error_msg.lower() or "401" in error_msg:
            return {"error": "Invalid API key. Please check your OPENAI_API_KEY or GROQ_API_KEY in the .env file."}
        if "model_decommissioned" in error_msg.lower() or "model" in error_msg.lower() and "not found" in error_msg.lower():
            return {"error": f"Model error: {error_msg}. Please check Groq documentation for available models: https://console.groq.com/docs/models"}
        return {"error": f"API Error: {error_msg}"}


def generate_trip_plan(travel_data: Any) -> Dict[str, Any]:
    """
    Generate a detailed trip plan based on travel data.
    
    Args:
        travel_data: TravelData object with trip information
        
    Returns:
        Dictionary with generated trip plan
    """
    if not client:
        return {"error": "API key not configured. Please set OPENAI_API_KEY or GROQ_API_KEY in your .env file"}
    
    try:
        travel_dict = travel_data.dict() if hasattr(travel_data, 'dict') else travel_data
        
        prompt = f"""Generate a detailed trip plan for:
        Destination: {travel_dict.get('destino', 'Unknown')}
        Start Date: {travel_dict.get('data_inicio', 'Unknown')}
        End Date: {travel_dict.get('data_fim', 'Unknown')}
        Travelers: {travel_dict.get('viajantes', 'Unknown')}
        Budget: {travel_dict.get('orçamento', 'Unknown')}
        Preferences: {travel_dict.get('preferencias', 'None')}
        
        Return a JSON object with daily itinerary."""
        
        # Use appropriate model based on API provider
        # Groq: llama-3.3-70b-versatile (replaces deprecated llama-3.1-70b-versatile)
        model = "llama-3.3-70b-versatile" if api_key and api_key.startswith("gsk_") else "gpt-4"
        
        response = client.chat.completions.create(
            model=model,
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
        error_msg = str(e)
        if "invalid_api_key" in error_msg.lower() or "401" in error_msg:
            return {"error": "Invalid API key. Please check your OPENAI_API_KEY or GROQ_API_KEY in the .env file."}
        if "model_decommissioned" in error_msg.lower() or "model" in error_msg.lower() and "not found" in error_msg.lower():
            return {"error": f"Model error: {error_msg}. Please check Groq documentation for available models: https://console.groq.com/docs/models"}
        return {"error": f"API Error: {error_msg}"}

