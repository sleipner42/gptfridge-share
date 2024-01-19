import inspect as core_inspect
from typing import List, Optional
from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declared_attr, declarative_base, mapped_column, Mapped

RootBase = declarative_base()


class BaseDB(RootBase):  # type: ignore

    __abstract__ = True
    _use_timestamps = True

    @classmethod
    def get_members(cls) -> List[str]:
        # getmembers() returns all the
        # members of an object
        members = []
        for i in core_inspect.getmembers(cls):
            # to remove private and protected
            # functions
            if not i[0].startswith("_"):
                # To remove other methods that
                # doesnot start with a underscore
                if not core_inspect.ismethod(i[1]):
                    members.append(i[0])

        return members

    @declared_attr
    def created_at(self) -> Mapped[datetime]:
        return (
            mapped_column(
                DateTime(timezone=True),
                nullable=False,
                server_default=func.now(),
            )
            if self._use_timestamps
            else None
        )

    @declared_attr
    def updated_at(self) -> Mapped[datetime]:
        return (
            mapped_column(
                DateTime(timezone=True),
                nullable=False,
                server_default=func.now(),
                onupdate=func.now(),
            )
            if self._use_timestamps
            else None
        )
