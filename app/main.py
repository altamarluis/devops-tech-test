from fastapi import FastAPI, status
from app.services import add_numbers

app = FastAPI(title="DevOps Automation Test App")

@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "ok"}

@app.get("/add", status_code=status.HTTP_200_OK)
def add(a: int, b: int):
    result = add_numbers(a, b)
    return {"result": result}