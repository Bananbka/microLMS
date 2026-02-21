from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RoleEntity:
    id: int
    name: str
    slug: str
    permissions: List[str]


@dataclass
class UserEntity:
    id: int
    email: str
    full_name: str
    phone: str
    role: Optional[str]
