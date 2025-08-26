from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Message": "Hello!! World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"Item ID": item_id}