from typing import List

from pydantic import BaseModel, Field


class User(BaseModel):
    username: str
    password: str
    active: bool = False
    roles: List[str] = Field([], description='a list of roles associated with the user')
