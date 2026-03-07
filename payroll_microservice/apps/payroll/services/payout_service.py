import pybreaker
from rest_framework.exceptions import ValidationError

from apps.payroll.infrastructure.repository import PayoutRepository
from apps.payroll.infrastructure.http_clients import check_user_exists


class PayoutService:
    def __init__(self, payout_repo=None):
        self.payout_repo = payout_repo or PayoutRepository()

    def get_all_payouts(self):
        return self.payout_repo.get_all()

    def get_payout(self, payout_id: int):
        return self.payout_repo.get_by_id(payout_id)

    def create_payout(self, data: dict, cookies: dict = None):
        try:
            check_user_exists(data['user'], cookies=cookies)
        except pybreaker.CircuitBreakerError:
            raise ValidationError({"detail": "User service is down (Circuit Open)."})

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
