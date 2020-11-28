from typing import Set

from pydantic import BaseModel


class JWTUser(BaseModel):
    username: str
    password: str
    active: bool = False
    roles: Set[str] = set()
