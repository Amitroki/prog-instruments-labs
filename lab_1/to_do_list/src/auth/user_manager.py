import uuid
import json
from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, UUIDIDMixin

from auth.models import User
from auth.utils import get_user_db
from auth.auth_backend import redis
from config import RESET_PASSWORD_TOKEN_SECRET, VERIFICATION_TOKEN_SECRET
from tasks.emails import (
    get_email_template_dashboard,
    send_email_report_dashboard
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """
    The user manager responsible for handling user-related events such as registration,
    password recovery, verification and login. It is based on the UUID as the user ID.

    Attributes:
        reset_password_token_secret (str): Secret key for generating a password reset token.
        verification_token_secret (str): The secret key for generating the email verification token.
    """
    reset_password_token_secret = RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = VERIFICATION_TOKEN_SECRET

    async def on_after_login(self, user: User,
                             request: Request | None = None,
                             response: Response | None = None
                             ) -> None:
        """ The method called after a successful user login.

        Args:
            user (User): The user who logged in.
            request (Optional[Request]): Facetapi request object (optional).
            response (Optional[Response]): A Facetapi response object containing a token (optional).

        Performs:
            Deletes the user's old Redis token and generates a new one for the current session.
        """
        response_body = response.body.decode('utf-8')
        response_body = json.loads(response_body)

        if user.redis_token_key is not None:
            await redis.delete(user.redis_token_key)
        key = f"fastapi_users_token:{response_body['access_token']}"
        await self._update(user, {"redis_token_key": key})

        print(f"user {user.id} has logined")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """ Method called after successful user registration.

        Args:
            user (User): A registered user.
            request (Optional[Request]): Facetapi request object (optional).

        Performs:
            Sends the user an email notification of registration.
        """
        content: str = f"<div>Dear {user.username}, you has been registred at ToDoList service</div>"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                             theme="Successful registration",
                                                             content=content)
        send_email_report_dashboard.delay(email)

        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """ The method called after the password reset request.

        Args:
            user (User): The user who requested a password reset.
            token (str): A token to reset the password.
            request (Optional[Request]): Facetapi request object (optional).

        Performs:
            Sends the user an email with a token to reset the password.
        """
        content: str = f"<div>Dear {user.username}, use this token to reset your password</div><div>{token}</div>"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                             theme="Password reset",
                                                             content=content)
        send_email_report_dashboard.delay(email)

        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_reset_password(self, user: User,
                                      request: Request | None = None
                                      ) -> None:
        """ The method called after a successful password reset.

        Args:
            user (User): The user who reset the password.
            request (Optional[Request]): Facetapi request object (optional).

        Performs:
            Sends the user an email with a notification about password reset.
        """
        content: str = f"<div>Dear {user.username}, your password has been reseted</div>"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                             theme="Successful password reset",
                                                             content=content)
        send_email_report_dashboard.delay(email)

        print(f"User {user.id} has reseted password")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """ The method called after the email verification request.

        Args:
            user (User): The user who requested verification.
            token (str): An email verification token.
            request (Optional[Request]): Facetapi request object (optional).

        Performs:
            Sends the user an email with a token for verification.
        """
        content: str = f"<div>Dear {user.username}, use this token to verify your password</div><div>{token}</div>"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                             theme="Email verification",
                                                             content=content)
        send_email_report_dashboard.delay(email)

        print(
            f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_verify(self, user: User, request: Request | None = None) -> None:
        """ Method called after successful email verification.

        Args:
            user (User): The user who verified the email.
            request (Optional[Request]): Facetapi request object (optional).

        Performs:
            Sends the user an email with verification confirmation.
        """
        content: str = f"<div>Dear {user.username}, your email has been verified"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                             theme="Successful email verification",
                                                             content=content)
        send_email_report_dashboard.delay(email)

        print(f"User {user.id} has been verified")


async def get_user_manager(user_db=Depends(get_user_db)):
    """ Function to get an instance of the User Manager.

    Args:
        user_db: Dependency for getting the user database.

    Yields:
        User Manager: An instance of the user manager.
    """
    yield UserManager(user_db)
