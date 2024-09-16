import uuid

from sqlalchemy import String, Integer, DATE, TIMESTAMP, UUID, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Item(Base):
    """ The model of the to-do item in the database.

    Attributes:
        __table name__ (str): The name of the table in the database ("item").
        id (Mapped[uuid.UUID]): A unique element identifier generated automatically.
        user_id (Mapped[uuid.UUID]): The foreign key that binds the element to the user.
        name (Mapped[str]): The name of the element.
        comment (Mapped[str]): Comment on the element. It may be empty.
        priority (Mapped[int]): The priority of the element (default is 0). It may be empty.
        do_till (Mapped[DATE | TIMESTAMP]): The date or time before which the element should be executed. It may be empty.
        is_done (Mapped[bool]): The execution status of the element (False by default).
        user (relationship): The relationship with the user model ("User"). Used to get the user who owns the item.
    """
    __tablename__ = 'item'
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=lambda: uuid.uuid4())
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String)
    comment: Mapped[str] = mapped_column(String, default=None, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    do_till: Mapped[DATE | TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), default=None, nullable=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    user = relationship("User", back_populates="to_do_items")
