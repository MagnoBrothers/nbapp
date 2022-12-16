import uuid
from typing import List, Optional
import datetime

from pydantic import BaseModel, Extra
from sqlmodel import Field, Relationship, SQLModel, Column, DateTime, func

from app.enums.job import Status
from app.schemas.basin import BasinCreate, BasinRead

from .base import Base


class JobBase(SQLModel):
    status: Status
    progr: int = Field(
        alias="progress", ge=0, le=100, sa_column_kwargs={"name": "progress"}
    )
    date: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow, nullable=False
    )

    class Config:
        allow_population_by_field_name = True


class JobDbRead(JobBase):
    id: uuid.UUID


class JobDbCreate(JobBase, extra=Extra.forbid):
    ...


class JobDbUpdate(JobBase):
    status: Optional[str]
    progr: Optional[int] = Field(
        alias="progress", ge=0, le=100, sa_column_kwargs={"name": "progress"}
    )


class JobDb(Base, JobBase, table=True):
    __tablename__ = "job"

    basin_id: uuid.UUID = Field(default=None, foreign_key="basin.id")
    basin: "BasinDb" = Relationship(back_populates="job")


# Routing Layer ###############


class JobRead(JobDbRead):
    basin: BasinRead


class JobCreate(BaseModel):
    basin: BasinCreate


class Links(BaseModel):
    prev: Optional[str]
    next: Optional[str]


class JobsRead(BaseModel):
    total: int
    # links: Links
    data: List[JobRead]
