from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


@dataclass
class PayoutAdjustmentEntity:
    id: int
    user: int
    name: str
    description: Optional[str]
    category: str
    amount: Decimal
    payout_id: Optional[int]
    created_at: datetime


@dataclass
class PayoutEntity:
    id: int
    user: int
    amount: Decimal
    status: str
    created_at: datetime
    adjustments: List[PayoutAdjustmentEntity] = field(default_factory=list)