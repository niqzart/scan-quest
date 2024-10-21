from pydantic import BaseModel

from app.config import Base
from tests.common.types import AnyJSON


def orm_to_json(model: type[BaseModel], entity: Base) -> AnyJSON:
    return model.model_validate(entity, from_attributes=True).model_dump(mode="json")
