from django.http import Http404
from rest_framework.exceptions import ValidationError

from apps.payroll.infrastructure.repository import PayoutAdjustmentRepository
from apps.users.services.user_service import UserService


class PayoutAdjustmentService:
    def __init__(self, adjustment_repo=None, user_service=None):
        self.adjustment_repo = adjustment_repo or PayoutAdjustmentRepository()
        self.user_service = user_service or UserService()

    def get_all_adjustments(self):
        return self.adjustment_repo.get_all()

    def get_adjustment(self, adjustment_id: int):
        return self.adjustment_repo.get_by_id(adjustment_id)

    def create_adjustment(self, data: dict):
        try:
            self.user_service.get_user(data['user'])
        except Http404:
            raise ValidationError({"user": ["There is no user with such id."]})

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
