# -*- coding: utf-8 -*-
from typing import Optional


from app.shared.service import BaseService
from app.modules.auth.repository import AuthRepository


class AuthService(BaseService):
    repo_class = AuthRepository

    async def register_user(
        self, username: str, password: str
    ) -> Optional[dict | bool]:
        # Implement your user registration logic here, e.g., save to a database
        # For demonstration, we'll just return True to indicate success
        user = await self.repository.create_user(
            username=username, email="", password=password
        )
        if user:
            return user

        return False

    async def authenticate_user(self, username: str, password: str) -> bool:
        # Implement your authentication logic here, e.g., check against a database
        # For demonstration, we'll just check against hardcoded values
        user = await self.repository.get_user_by_username(username)
        if user and user["password"] == password:
            return True
        return False
