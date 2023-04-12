from typing import Optional
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions
from sqlalchemy_utils import database_exists, create_database


class Base(DeclarativeBase):
    pass


class Metadata(Base):
    __tablename__ = "metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=functions.now())
    make: Mapped[str]
    model: Mapped[str]
    product_url: Mapped[str]
    image_url: Mapped[str]
    image_filename: Mapped[str]
    s3_url: Mapped[Optional[str]] = mapped_column(default=None)


class Database:
    def __init__(self, local: bool = True) -> None:
        if local:
            self._engine = create_engine("sqlite:///sqlite3.db", echo=False)
        else:
            raise NotImplementedError

        if not database_exists(self._engine.url):
            create_database(self._engine.url)
            Base.metadata.create_all(self._engine)
        self._session_maker = sessionmaker(bind=self._engine)

    def add_to_db(self, metadata: Metadata) -> None:
        with self._session_maker() as session:
            session.add(metadata)
            session.commit()

    def image_exists(self, product_url: str) -> bool:
        with self._session_maker() as session:
            statement = Select(Metadata).where(Metadata.product_url == product_url)
            if session.execute(statement).one_or_none():
                return True
            return False
