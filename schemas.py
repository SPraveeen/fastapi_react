from pydantic import BaseModel

class TaskSchema(BaseModel):
    taskname: str
    description: str
    status: str