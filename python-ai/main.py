import os
from fastapi import FastAPI, Request,HTTPException, Response
from fastapi.responses import JSONResponse
from models import ParseInput, TravelData, SaveRoteiroInput
from services.ai_service import parse_trip_request, generate_trip_plan
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="TripWave AI Backend")

@app.post("/parse")
def parse_trip(data: ParseInput):
    try:
        if not data.mensagem or data.mensagem.strip() == "":
            raise HTTPException(status_code=400, detail="O campo 'mensagem' não pode estar vazio")
        return parse_trip_request(data.mensagem)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a requisição: {str(e)}")
    