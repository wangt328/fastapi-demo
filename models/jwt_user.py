from typing import List

from pydantic import BaseModel


class JWTUser(BaseModel):
    username: str
    password: str
    active: bool = False
    roles: List[str] = []
