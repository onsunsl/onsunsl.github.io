from pydantic import BaseModel, Field

class A(BaseModel):
    a: str = "123"
    sub_a: "A" = None



a = A(sub_a=A(a="3224"))
print(a)

