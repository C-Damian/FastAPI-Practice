from typing import Optional, List
from fastapi import FastAPI
from enum import IntEnum
from pydantic import BaseModel, Field

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=50, description="Name of the todo item")
    todo_description: str = Field(..., min_length=3, max_length=100, description="Description of the todo item"),
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority of the todo item")

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description="ID of the todo item")

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, description="Priority of the todo item") 
    todo_description: Optional[str] =Field(None, description="Priority of the todo item")  
    priority: Optional[Priority] = Field(None, description="Priority of the todo item") 

all_todos = [
    Todo(todo_id=1, todo_name="Sports", todo_description="Play football", priority=Priority.HIGH),
    Todo(todo_id=2, todo_name="Music", todo_description="Listen to jazz", priority=Priority.MEDIUM),
    Todo(todo_id=3, todo_name="Study", todo_description="Read FastAPI documentation", priority=Priority.LOW),
    Todo(todo_id=4, todo_name="Shopping", todo_description="Buy groceries", priority=Priority.HIGH),
    Todo(todo_id=5, todo_name="Cleaning", todo_description="Clean the house", priority=Priority.MEDIUM)
]

app = FastAPI()

#Query parameters
@app.get("/age")
def query(age: int = None):
    if age < 21:
        return {"Message": f"Hello, Sorry, you cannot drink, since you're {age}!"}
    if age >= 21:
        return {"Message": f"Hello, You can drink, since you're {age}!"}

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo

@app.get("/todos", response_model=List[Todo])
def get_todos(first_n: int = None):
    if first_n is not None:
        return all_todos[:first_n]
    return all_todos

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1

    new_todo = Todo(
        todo_id=new_todo_id,
        todo_name=todo.todo_name,
        todo_description=todo.todo_description,
        priority=todo.priority
    )

    all_todos.append(new_todo)
    return new_todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            todo.todo_name = updated_todo.todo_name
            todo.todo_description = updated_todo.todo_description
            todo.priority = updated_todo.priority
            return todo
    return {"Message": "You cannot update todos that don't exist!"}
    
@app.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            all_todos.remove(todo)
            return todo
    return {"Message": "You cannot delete todos that don't exist!"}