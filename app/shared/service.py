from typing import Type, TypeVar, Any
from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core.database import get_session

T = TypeVar("T", bound="BaseService")


class BaseService:
    """
    The ultimate base class for all domain services.
    Handles constructor initialization and automatic FastAPI dependency generation.
    """

    # Force subclasses to define which repository they belong to
    repo_class: Type[Any] = None

    def __init__(self, repository: Any):
        """Automatically assigns the repository to self.repository for all services."""
        self.repository = repository

    @classmethod
    def as_dependency(cls: Type[T]):
        """Generates the nested factory function for FastAPI's Depends()."""
        if cls.repo_class is None:
            raise ValueError(
                f"Class {cls.__name__} must define 'repo_class' to use BaseService."
            )

        def _get_service(session: AsyncSession = Depends(get_session)) -> T:
            # 1. Spin up the repository using the request's DB session
            repository = cls.repo_class(session)
            # 2. Instantly spin up the service using that repository
            return cls(repository)

        return _get_service
