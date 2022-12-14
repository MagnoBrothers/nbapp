import uuid
from typing import Optional

from pydantic import Extra
from sqlmodel import Field, Relationship, SQLModel

from .base import Base


class BasinBase(SQLModel):
    name: str
    imw: int
    imh: int
    coefs: str
    crmin: float
    crmax: float
    cimin: float
    cimax: float
    itmax: int
    tol: float


class BasinDbRead(BasinBase):
    id: uuid.UUID
    image_url: str
    thumbnail_url: str


class BasinDbCreate(BasinBase, extra=Extra.ignore):
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None


class BasinDbUpdate(BasinBase):
    name: Optional[str]
    imw: Optional[int]
    imh: Optional[int]
    coefs: Optional[str]
    crmin: Optional[float]
    crmax: Optional[float]
    cimin: Optional[float]
    cimax: Optional[float]
    itmax: Optional[int]
    tol: Optional[float]
    image_url: Optional[str]
    thumbnail_url: Optional[str] = None


class BasinDb(Base, BasinBase, table=True):
    __tablename__ = "basin"

    image_url: Optional[str] = Field(default=None)
    thumbnail_url: Optional[str] = Field(default=None)

    job: "JobDb" = Relationship(back_populates="basin")


# Routing Layer ###############


class BasinRead(BasinBase):
    id: uuid.UUID
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None


class BasinCreate(BasinBase):
    ...

    class Config:
        schema_extra = {
            "example": {
                "name": "Basin name",
                "imw": 32,
                "imh": 32,
                "coefs": "[1, 0, 0, 0, 1]",
                "crmin": -1.1,
                "crmax": 1.1,
                "cimin": -1.1,
                "cimax": 1.1,
                "itmax": 30,
                "tol": 1e-6,
            }
        }
