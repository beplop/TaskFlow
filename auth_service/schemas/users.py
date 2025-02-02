from pydantic import BaseModel, ConfigDict


class UserSchemaAdd(BaseModel):
    name: str
    password: str


class UserSchema(UserSchemaAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
