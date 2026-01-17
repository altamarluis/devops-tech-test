
##testing workflow

from fastapi import FastAPI
from app.services import add_numbers

app = FastAPI(title="DevOps Automation Test App")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/add")
def add(a: int, b: int):
    result = add_numbers(a, b)
    return {"result": result}
