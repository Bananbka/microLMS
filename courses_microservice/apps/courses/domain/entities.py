from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional
from datetime import datetime


@dataclass
class LessonEntity:
    id: int
    topic: str
    html_content: str
    course_id: int
    author_id: Optional[int]
    created_at: datetime
    updated_at: datetime


@dataclass
class CourseEntity:
    id: int
    title: str
    description: Optional[str]
    is_active: bool
    author_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    lessons: List[LessonEntity] = field(default_factory=list)
    price: Decimal = Decimal(0)


@dataclass
class CoursePurchaseEntity:
    id: int
    user_id: int
    course: int
    price_at_moment: Decimal
    status: str
    error_message: str
    created_at: datetime
    updated_at: datetime
