from pydantic import BaseModel, Field
from uuid import uuid4


def str_uuid() -> str:
    return str(uuid4())


class A(BaseModel):
    a: str = Field(default_factory=lambda x: str(uuid4()))


print(A().a)
