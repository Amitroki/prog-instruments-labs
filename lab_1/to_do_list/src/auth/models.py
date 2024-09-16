from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """ A user model using SQLAlchemy with UUID as the identifier.

    Attributes:
        __table name__ (str): The name of the table in the database ("user").
        username (Mapped[str]): The user's name. Cannot be empty (nullable=False).
        redis_token_key (Mapped[str]): The token key in Redis. It can be empty (nullable=True), used to store the associated token.
        to_do_items (relationship): A one-to-many relationship with Item objects. Allows you to receive the user's tasks (to-do) through feedback.
    """
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(String, nullable=False)
    redis_token_key: Mapped[str] = mapped_column(
        String, default=None, nullable=True)
    to_do_items = relationship("Item", back_populates="user")
