from typing import Any
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase
import json


class Base(DeclarativeBase):
    def to_dict(self) -> dict[str, Any]:
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self).mapper.column_attrs
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
