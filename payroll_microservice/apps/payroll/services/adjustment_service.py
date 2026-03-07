import pybreaker
from rest_framework.exceptions import ValidationError

from apps.payroll.infrastructure.repository import PayoutAdjustmentRepository
from apps.payroll.infrastructure.http_clients import check_user_exists


class PayoutAdjustmentService:
    def __init__(self, adjustment_repo=None):
        self.adjustment_repo = adjustment_repo or PayoutAdjustmentRepository()

    def get_all_adjustments(self):
        return self.adjustment_repo.get_all()

    def get_adjustment(self, adjustment_id: int):
        return self.adjustment_repo.get_by_id(adjustment_id)

    def create_adjustment(self, data: dict):
        try:
            check_user_exists(data['user'])
        except pybreaker.CircuitBreakerError:
            raise ValidationError({"detail": "User service is down (Circuit Open)."})

        return self.adjustment_repo.create(
            user=data['user'],
            name=data['name'],
            category=data['category'],
            amount=data['amount'],
            description=data.get('description'),
            payout_id=data.get('payout_id')
        )

    def update_adjustment(self, adjustment_id: int, update_data: dict):
        return self.adjustment_repo.update(adjustment_id, update_data)

    def delete_adjustment(self, adjustment_id: int):
        self.adjustment_repo.delete(adjustment_id)
