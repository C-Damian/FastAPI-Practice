from fastapi import FastAPI
from enum import Enum

all_todos = [
    {"todo_id": 1, "todo_name": "Sports", "todo_description": "Play football"},
    {"todo_id": 2, "todo_name": "Music", "todo_description": "Listen to jazz"},
    {"todo_id": 3, "todo_name": "Study", "todo_description": "Read FastAPI documentation"},
    {"todo_id": 4, "todo_name": "Shopping", "todo_description": "Buy groceries"},
    {"todo_id": 5, "todo_name": "Cleaning", "todo_description": "Clean the house"}
]

class ModelName(str, Enum):
    alexnet= "AlexNet"
    resnet= "ResNet"
    lenet= "LeNet"

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Message": "Hello!! World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"Item ID": item_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "LeNet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    elif model_name == ModelName.resnet:
        return {"model_name": model_name, "message": "wadaloplaplap."}

#Query parameters
@app.get("/age")
def query(age: int = None):
    if age < 21:
        return {"Message": f"Hello, Sorry, you cannot drink, since you're {age}!"}
    if age >= 21:
        return {"Message": f"Hello, You can drink, since you're {age}!"}

@app.get("/todos")
def get_todos(first_n: int = None):
    if first_n is not None:
        return {"todos": all_todos[:first_n]}
    return {"todos": all_todos}
    
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    todo = next((item for item in all_todos if item["todo_id"] == todo_id), None)
    if todo:
        return {"todo": todo}
    return {"Message": "Todo not found"}

@app.post("/todos")
def create_todo(todo: dict):
    new_todo_id = max(todo["todo_id"] for todo in all_todos) + 1

    new_todo = {
        "todo_id": new_todo_id,
        "todo_name": todo["todo_name"],
        "todo_description": todo["todo_description"]
    }
    all_todos.append(new_todo)
    return {"todo": new_todo}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: dict):
    for todo in all_todos:
        if todo["todo_id"] == todo_id:
            todo["todo_name"] = updated_todo["todo_name"]
            todo["todo_description"] = updated_todo["todo_description"]
            return {"message": "Todo updated successfully", "todo": todo}
    return {"Message": "You cannot update todos that don't exist!"}
    
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for todo in all_todos:
        if todo["todo_id"] == todo_id:
            all_todos.remove(todo)
            return {"message": "Todo deleted successfully", "todo": todo}
    return {"Message": "You cannot delete todos that don't exist!"}