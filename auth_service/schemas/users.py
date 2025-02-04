from pydantic import BaseModel, ConfigDict


class AddUserSchema(BaseModel):
    name: str
    password: str


class UserSchema(AddUserSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
