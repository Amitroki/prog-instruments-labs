import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """ A schema for reading user data.

    Inherits:
        schema.BaseUser[uuid.UUID]: Base class for users with UUID as an identifier.

    Attributes:
        username (user): The user's name.
    """    
    username: str


class UserCreate(schemas.BaseUserCreate):
    """ Scheme for creating a new user.

    Inherits:
        schemas.BaseUserCreate: The base class for creating users.

    Attributes:
        username (user): The user's name.
    """
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    """ Schema for updating user data.

    Inherits:
        schemas.BaseUserUpdate: The base class for updating users.

    Attributes:
        username (user): The user's name.
    """
    username: str
