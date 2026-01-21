from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.services import add_numbers

app = FastAPI(title="DevOps Automation Test App")

# Serve frontend (frontend/index.html)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/add")
def add(a: int, b: int):
    result = add_numbers(a, b)
    return {"result": result}
