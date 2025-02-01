from pydantic import BaseModel, ConfigDict


class TaskSchemaAdd(BaseModel):
    title: str
    author_id: int
    description: str | None
    assignee_id: int | None


class TaskSchema(TaskSchemaAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
