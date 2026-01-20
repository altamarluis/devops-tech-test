from fastapi import FastAPI
from app.services import subtract_numbers

app = FastAPI(title="DevOps Automation Test App")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/subtract")
def subtract(a: int, b: int):
    result = subtract_numbers(a, b)
    return {"result": result}