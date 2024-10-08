# route.py

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from database import existing_todos

router = APIRouter(prefix="/todo")

# Define a ToDo model
class ToDoItem(BaseModel):
    id: int = None
    title: str
    description: str = None
    is_completed: bool = False

# Create a ToDo item
@router.post("/", summary="Create a new ToDo item")
def create_todo(item: ToDoItem):
    item.id = len(existing_todos) + 1
    existing_todos.append(item.model_dump())
    return {"message": "ToDo item created", "todo": item}

# Get all ToDo items or filter by completed status (using query parameter)
@router.get("/", summary="Retrieve ToDo items")
def get_todos(is_completed: bool = Query(None, description="Filter by completion status")):
    if is_completed is None:
        return {"todos": existing_todos}
    filtered_todos = [todo for todo in existing_todos if todo["is_completed"] == is_completed]
    return {"todos": filtered_todos}

# Update a ToDo item by id (using path parameter)
@router.put("/{todo_id}", summary="Update an existing ToDo item")
def update_todo(todo_id: int, item: ToDoItem):
    for todo in existing_todos:
        if todo["id"] == todo_id:
            todo.update(item.model_dump())
            return {"message": "ToDo item updated", "todo": todo}
    raise HTTPException(status_code=404, detail="ToDo item not found")

# Delete a ToDo item by id (using path parameter)
@router.delete("/{todo_id}", summary="Delete a ToDo item")
def delete_todo(todo_id: int):
    for index, todo in enumerate(existing_todos):
        if todo["id"] == todo_id:
            del existing_todos[index]
            return {"message": "ToDo item deleted"}
    raise HTTPException(status_code=404, detail="ToDo item not found")