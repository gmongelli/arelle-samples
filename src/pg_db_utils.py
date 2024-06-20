import datetime

from sqlalchemy import create_engine, Engine, ForeignKey, Index, String, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import Mapped, mapped_column
from typing import Any

from models.base import Base

class Document(Base):
    __tablename__ = 'documents'

    name: Mapped[str] = mapped_column()

class Fact(Base):
    __tablename__ = 'facts'

    # relations
    id_document: Mapped[int] = mapped_column(ForeignKey(Document.id), index=True)
    # columns
    value: Mapped[str] = mapped_column(nullable=True)
    decimals: Mapped[int] = mapped_column(nullable=True)
    concept: Mapped[str] = mapped_column(index=True)
    entity: Mapped[str] = mapped_column(nullable=True)
    period_start: Mapped[datetime.datetime] = mapped_column(nullable=True)
    period_end: Mapped[datetime.datetime] = mapped_column(nullable=True)
    unit: Mapped[str] = mapped_column(String(255), nullable=True)
    language: Mapped[str] = mapped_column(String(16))
    id_note: Mapped[str] = mapped_column(nullable=True)
    dimensions: Mapped[dict[str, Any]] = mapped_column(nullable=True)
    links: Mapped[dict[str, Any]] = mapped_column(nullable=True)
    # indices

    __table_args__ = (
        Index('facts_dimensions_ndx',
              dimensions,
              postgresql_using="gin",
              postgresql_ops={
                  'dimensions': 'jsonb_path_ops'
              }
              ),
    )
def init_DB(pg_user:str, pg_password:str, pg_host:str, pg_port: str, pg_database:str) -> Engine:
    print(f'Connecting to database {pg_database}')
    engine = create_engine(f'postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}')
    Base.metadata.create_all(engine)
    return engine

def connect_DB(pg_user:str, pg_password:str, pg_host:str, pg_port: str, pg_database:str) -> Engine:
    print(f'Opening connection to database {pg_database}')
    engine = create_engine(f'postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}')
    return engine

def session_factory(engine: Engine) -> Session:
    Session = sessionmaker(engine)
    return Session

def delete_all(session_factory) -> None:
    with session_factory.begin() as session:
        for table in Base.metadata.tables.keys():
            session.execute(text(f'TRUNCATE TABLE {table} CASCADE'))


def insert_document(session_factory, name: str) -> int:
    with session_factory.begin() as session:
        document = Document()
        document.name = name
        session.add(document)
        session.flush()
        session.refresh(document)
        return document.id
def insert_fact(session_factory,
                document_id: int,
                value: str,
                decimals: str,
                concept: str,
                entity: str,
                period_start: datetime.datetime,
                period_end: datetime.datetime,
                unit: str,
                language: str,
                dimensions: dict[str, str]) -> None:
    with session_factory.begin() as session:
        fact = Fact()
        fact.id_document = document_id
        fact.value = value
        if decimals is not None and isinstance(decimals, int) :
            fact.decimals = decimals
        fact.concept = concept
        if entity:
            fact.entity = entity
        if period_start:
            fact.period_start = period_start
        if period_end:
            fact.period_end = period_end
        if unit:
            fact.unit = unit
        fact.language = language
        if dimensions:
            fact.dimensions = dimensions
        session.add(fact)