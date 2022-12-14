import datetime
import uuid

from sqlmodel import Column, DateTime, Field, SQLModel, func


class Base(SQLModel):

    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    )
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
    )
