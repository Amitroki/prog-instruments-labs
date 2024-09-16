from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID


class ItemCreate(BaseModel):
    """ Scheme for creating a new to-do list item.

    Attributes:
        name (str): The name of the element.
        comment (Optional[str]): Comment on the element. It may be empty.
        priority (int): The priority of the element should be in the range from 0 to 10 (default is 0).
        do_till (Optional[datetime]): The date or time before which the element must be executed. It may be empty.
    """
    name: str
    comment: Optional[str]
    priority: int = Field(le=10, ge=0, default=0)
    do_till: Optional[datetime]


class ItemRead(ItemCreate):
    """ Schema for reading the data of a to-do list item.

    Inheritsfrom:
        ItemCreate: A scheme for creating a to-do list item by adding ID and progress status attributes.

    Attributes:
        id (UUID): The unique identifier of the element.
        is_done (bool): The execution status of the element.
    """
    id: UUID
    is_done: bool


class ItemUpdate(ItemCreate):
    """ Schema for updating the data of a to-do list item.

    Inheritsfrom:
        ItemCreate: A scheme for creating a to-do list item, adding the ability to update the name.

    Attributes:
        name (Optional[str]): The new name of the element. It may be empty.
    """
    name: Optional[str]
