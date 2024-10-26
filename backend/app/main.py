from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Productos111"}

@app.get("/productos")
def get_products():
    return {"productos": "platano"}


@app.get("/productos/capy")
def get_products():
    return {"productos": "capy"}