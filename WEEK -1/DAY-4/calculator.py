from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Calculator API",
    description="Simple calculator built with FastAPI",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Calculator API is running"
    }


@app.get("/add")
def add(a: float, b: float):
    result = a + b

    return {
        "operation": "addition",
        "a": a,
        "b": b,
        "result": result
    }


@app.get("/subtract")
def subtract(a: float, b: float):
    result = a - b

    return {
        "operation": "subtraction",
        "a": a,
        "b": b,
        "result": result
    }


@app.get("/multiply")
def multiply(a: float, b: float):
    result = a * b

    return {
        "operation": "multiplication",
        "a": a,
        "b": b,
        "result": result
    }


@app.get("/divide")
def divide(a: float, b: float):

    if b == 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot divide by zero"
        )

    result = a / b

    return {
        "operation": "division",
        "a": a,
        "b": b,
        "result": result
    }