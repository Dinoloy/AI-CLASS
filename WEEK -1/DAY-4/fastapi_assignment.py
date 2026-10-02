from fastapi import FastAPI

app = FastAPI(
    title="My First FastAPI App",
    description="A simple beginner FastAPI project",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to my first FastAPI application!"
    }


@app.get("/greet/{name}")
def greet(name: str):
    return {
        "message": f"Hello, {name}!"
    }


@app.get("/add")
def add(a: float, b: float):
    return {
        "a": a,
        "b": b,
        "result": a + b
    }
