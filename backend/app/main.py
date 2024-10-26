from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Productos111"}



@app.get("/prueba")
def read_root():
    return {"Hello1": "capy"}