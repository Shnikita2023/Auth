from abc import abstractmethod, ABC

from application.repos.ad import AbstractAdvertisementRepository, SQLAlchemyAdvertisementRepository
from application.repos.category_ad import AbstractCategoryAdRepository, SQLAlchemyCategoryAdRepository
from application.repos.moderation import AbstractModerationRepository, SQLAlchemyModerationRepository
from application.repos.user import AbstractUserRepository, SQLAlchemyUserRepository


class AbstractUnitOfWork(ABC):
    users: AbstractUserRepository
    category: AbstractCategoryAdRepository
    advertisement: AbstractAdvertisementRepository
    moderation: AbstractModerationRepository

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> None:
        self.session = self.session_factory()
        self.users = SQLAlchemyUserRepository(self.session)
        self.category = SQLAlchemyCategoryAdRepository(self.session)
        self.advertisement = SQLAlchemyAdvertisementRepository(self.session)
        self.moderation = SQLAlchemyModerationRepository(self.session)

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
