from rest_framework.exceptions import ValidationError
from django.http import Http404

from apps.payroll.infrastructure.repository import PayoutRepository
from apps.users.services.user_service import UserService


class PayoutService:
    def __init__(self, payout_repo=None, user_service=None):
        self.payout_repo = payout_repo or PayoutRepository()
        self.user_service = user_service or UserService()

    def get_all_payouts(self):
        return self.payout_repo.get_all()

    def get_payout(self, payout_id: int):
        return self.payout_repo.get_by_id(payout_id)

    def create_payout(self, data: dict):
        try:
            self.user_service.get_user(data['user'])
        except Http404:
            raise ValidationError({"user": ["There is no user with such id."]})

        return self.payout_repo.create(
            user=data['user'],
            amount=data['amount'],
            status=data.get('status', 'PENDING')
        )

    def update_payout(self, payout_id: int, update_data: dict):
        payout = self.payout_repo.get_by_id(payout_id)
        if payout.status == 'PAID':
            raise ValidationError({"detail": "Cannot edit payout that was payed."})

        return self.payout_repo.update(payout_id, update_data)

    def delete_payout(self, payout_id: int):
        payout = self.payout_repo.get_by_id(payout_id)
        if payout.status == 'PAID':
            raise ValidationError({"detail": "Cannot delete payout that was payed."})

        self.payout_repo.delete(payout_id)
