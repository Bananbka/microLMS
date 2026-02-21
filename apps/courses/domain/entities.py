from dataclasses import dataclass
from typing import Optional


@dataclass
class CourseEntity:
    title: str
    description: str
    id: Optional[int] = None
