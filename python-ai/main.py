from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/parse")
def parse_trip(request: Request):
    body =  request.json() 
    print(body)