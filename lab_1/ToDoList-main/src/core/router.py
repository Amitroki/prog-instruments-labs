from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from main import fastapi_users
from core.schemas import ItemCreate, ItemRead, ItemUpdate
from database import get_async_session
from core.models import Item
from auth.models import User


router = APIRouter(
    prefix="/todo",
    tags=["ToDoList"]
)

current_user = fastapi_users.current_user()


@router.post("/add_item")
async def add_item_to_list(item: ItemCreate,
                           session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):
    """ Adds a new item to the user's to-do list.

    Args:
        item (ItemCreate): Data for creating a new item.
        session (AsyncSession): An asynchronous database session provided via Depends.
        user (User): The current authenticated user provided via Depends.

    Performs:
        Adds a new item to the database and associates it with the current user.
    """
    item_db = Item(**item.model_dump(), user_id=user.id)
    session.add(item_db)
    await session.commit()


@router.get("/get_items", response_model=list[ItemRead])
async def get_items(sort_by: list[str] = Query(default=["do_till", "1"],
                                               max_length=2,
                                               min_length=2),
                    user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):
    """ Returns a list of the current user's to-do items with the ability to sort.

    Args:
        sort_by (list[str]): Sorting parameters consisting of the sorting field ("priority", "do_till")
                             and the sorting direction (1 - ascending, 0 - descending).
        user (User): The current authenticated user provided via Depends.
        session (AsyncSession): An asynchronous database session provided via Depends.

    Returns:
        list[Item Read]: A sorted list of the user's to-do items.

    Raises:
        HttpException: If the sorting parameters are incorrect.
    """
    if sort_by[0] not in (None, "priority", "do_till"):
        raise HTTPException(422)
    try:
        sort_by[1] = int(sort_by[1])
    except:
        raise HTTPException(422)

    query = select(User).options(joinedload(
        User.to_do_items)).filter(user.id == User.id)
    user_with_items = await session.execute(query)
    user_with_items = user_with_items.unique().scalars().first()

    res = [ItemRead.model_validate(i, from_attributes=True)
           for i in user_with_items.to_do_items]

    if sort_by[1] != 0:
        res.sort(key=lambda x: getattr(x, sort_by[0]),
                 reverse=True if sort_by[1] > 0 else False)

    return res


@router.post("/marks_as_done")
async def mark(item_id: UUID,
               user: User = Depends(current_user),
               session: AsyncSession = Depends(get_async_session)
               ):
    """ Marks the to-do list item as completed.

    Args:
        item_id (UUID): ID of the to-do list item.
        user (User): The current authenticated user provided via Depends.
        session (AsyncSession): An asynchronous database session provided via Depends.

    Performs:
        Changes the status of the item to "completed" if it belongs to the current user.
    """
    item_db = await session.get(Item, item_id)

    if item_db.user_id != user.id:
        return
    item_db.is_done = True
    await session.commit()


@router.patch("/update_item")
async def update_item(item_id: UUID,
                      new_item: ItemUpdate,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)
                      ):
    """ Updates the data of the to-do list item.

    Args:
        item_id (UUID): ID of the to-do list item.
        new_item (Item Update): Updated data for the item.
        user (User): The current authenticated user provided via Depends.
        session (AsyncSession): An asynchronous database session provided via Depends.

    Performs:
        Updates the item data if it belongs to the current user.
    """
    item_db = await session.get(Item, item_id)
    if item_db.user_id != user.id:
        return
    to_upd = new_item.model_dump()
    for field, val in to_upd.items():
        if val is not None:
            setattr(item_db, field, val)
    await session.commit()


@router.delete("/delete_item")
async def delete_item(item_id,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)
                      ):
    """ Deletes an item from the to-do list.

    Args:
        item_id (UUID): ID of the to-do list item.
        user (User): The current authenticated user provided via Depends.
        session (AsyncSession): An asynchronous database session provided via Depends.

    Performs:
        Deletes an item if it belongs to the current user.
    """
    item_db = await session.get(Item, item_id)
    if item_db.user_id != user.id:
        return
    await session.delete(item_db)
    await session.commit()
