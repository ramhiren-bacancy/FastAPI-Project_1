from fastapi import APIRouter,Depends, HTTPException,status
from sqlalchemy import select
from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.todo import Todo
from app.models.user import User
from app.schemas.response import ApiResponse
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.utils.dependencies import get_current_user
from app.utils.error_decorator import db_exception_handler
from app.utils.response import api_response
from database import get_db


router = APIRouter()



# ? Create a new todo item

@router.post("/", response_model=ApiResponse[TodoResponse], status_code=status.HTTP_201_CREATED)
@db_exception_handler
async def create_todo(todo: TodoCreate, session: Annotated[AsyncSession, Depends(get_db)],current_user: User = Depends(get_current_user)):
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        user_id=current_user.id 
    )

    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo)

    return api_response(
        status_code=201,
        message="Todo is Created successfully",
        data=new_todo
    )


# ? Get all todo items
@router.get("/",response_model=ApiResponse[list[TodoResponse]],  status_code=status.HTTP_200_OK)
@db_exception_handler
async def get_all_todos(session: Annotated[AsyncSession, Depends(get_db)],current_user: User = Depends(get_current_user)):
    result = await session.execute(select(Todo).where(Todo.user_id == current_user.id))
    todos = result.scalars().all()
    return api_response(
        status_code=200,
        message="Todos fetched successfully",
        data=todos
    )
    # return todos

# ? Get a specific todo item by ID
@router.get("/{todo_id}", response_model=ApiResponse[TodoResponse], status_code=status.HTTP_200_OK)
@db_exception_handler
async def get_todo_by_id(todo_id: int, session: Annotated[AsyncSession, Depends(get_db)],current_user: User = Depends(get_current_user)):
    result = await session.execute(select(Todo).where(Todo.id == todo_id,Todo.user_id == current_user.id))
    todo = result.scalars().first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo is not Found")
    return api_response(
        status_code=200,
        message="Todo Fetched successfully",
        data=todo
    )

# ? Patch Route
@router.patch("/{todo_id}",response_model=ApiResponse[TodoResponse], status_code=status.HTTP_201_CREATED)
@db_exception_handler
async def update_todo(todo_id:int, todo_data:TodoUpdate, session:Annotated[AsyncSession,Depends(get_db)],current_user: User = Depends(get_current_user)):
    result = await session.execute(select(Todo).where(Todo.id == todo_id,Todo.user_id == current_user.id))
    print(result)
    todo = result.scalars().first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo is not Found")
    
    update_todo = todo_data.model_dump(exclude_unset=True)
    
    for field,value in update_todo.items():
        setattr(todo,field,value)
    
    await session.commit()
    await session.refresh(todo)
    return api_response(
        status_code=201,
        message="Todo Edit successfully",
        data=todo
    )  


@router.patch("/toggle/{todo_id}", response_model=ApiResponse[TodoResponse])
@db_exception_handler
async def toggel_todo(todo_id:int, session:Annotated[AsyncSession,Depends(get_db)],current_user: User = Depends(get_current_user)):
    result= await session.execute(select(Todo).where(Todo.id == todo_id,Todo.user_id == current_user.id))
    todo = result.scalars().first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo is not Found")
    
    todo.is_completed = not todo.is_completed
    
    await session.commit()
    await session.refresh(todo)
    
    return api_response(
        status_code=200,
        message="Todo Toggel successfully",
        data=todo
    )



# ? Delete Specific todo item by ID
@router.delete("/{todo_id}", response_model=ApiResponse[None], status_code=status.HTTP_200_OK)
@db_exception_handler
async def delete_todo(todo_id:int, session: Annotated[AsyncSession,Depends(get_db)],current_user: User = Depends(get_current_user)):
    result = await session.execute(select(Todo).where(Todo.id == todo_id,Todo.user_id == current_user.id))
    todo = result.scalars().first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo is not Found")
    
    await session.delete(todo)
    await session.commit()
    
    return api_response(
        status_code=200,
        message="Todo deleted successfully",
        data=None
    )