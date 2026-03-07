from decimal import Decimal
from django.shortcuts import get_object_or_404

from ..domain.entities import PayoutEntity, PayoutAdjustmentEntity
from .models import Payout, PayoutAdjustment


class PayoutRepository:
    def _adjustment_to_entity(self, adjustment: PayoutAdjustment) -> PayoutAdjustmentEntity:
        return PayoutAdjustmentEntity(
            id=adjustment.id,
            user=adjustment.user,
            name=adjustment.name,
            description=adjustment.description,
            category=adjustment.category,
            amount=adjustment.amount,
            payout_id=adjustment.payout_id,
            created_at=adjustment.created_at
        )

    def _payout_to_entity(self, payout: Payout) -> PayoutEntity:
        return PayoutEntity(
            id=payout.id,
            user=payout.user,
            amount=payout.amount,
            status=payout.status,
            created_at=payout.created_at,
            adjustments=[self._adjustment_to_entity(a) for a in payout.adjustments.all()]
        )

    def get_all(self) -> list[PayoutEntity]:
        payouts = Payout.objects.prefetch_related('adjustments').all()
        return [self._payout_to_entity(p) for p in payouts]

    def get_by_id(self, payout_id: int) -> PayoutEntity:
        payout = get_object_or_404(Payout.objects.prefetch_related('adjustments'), id=payout_id)
        return self._payout_to_entity(payout)

    def create(self, user: int, amount: Decimal, status: str = 'PENDING') -> PayoutEntity:
        payout = Payout.objects.create(
            user=user,
            amount=amount,
            status=status
        )
        return self._payout_to_entity(payout)

    def update(self, payout_id: int, update_data: dict) -> PayoutEntity:
        payout = get_object_or_404(Payout, id=payout_id)

        for key, value in update_data.items():
            setattr(payout, key, value)

        payout.save()
        return self._payout_to_entity(payout)

    def delete(self, payout_id: int) -> None:
        payout = get_object_or_404(Payout, id=payout_id)
        payout.delete()


class PayoutAdjustmentRepository:
    def _to_entity(self, adjustment: PayoutAdjustment) -> PayoutAdjustmentEntity:
        return PayoutAdjustmentEntity(
            id=adjustment.id,
            user=adjustment.user,
            name=adjustment.name,
            description=adjustment.description,
            category=adjustment.category,
            amount=adjustment.amount,
            payout_id=adjustment.payout_id,
            created_at=adjustment.created_at
        )

    def get_all(self) -> list[PayoutAdjustmentEntity]:
        adjustments = PayoutAdjustment.objects.all()
        return [self._to_entity(a) for a in adjustments]

    def get_by_id(self, adjustment_id: int) -> PayoutAdjustmentEntity:
        adjustment = get_object_or_404(PayoutAdjustment, id=adjustment_id)
        return self._to_entity(adjustment)

    def create(self, user: int, name: str, category: str, amount: Decimal,
               description: str = None, payout_id: int = None) -> PayoutAdjustmentEntity:
        adjustment = PayoutAdjustment.objects.create(
            user=user,
            name=name,
            description=description,
            category=category,
            amount=amount,
            payout_id=payout_id
        )
        return self._to_entity(adjustment)

    def update(self, adjustment_id: int, update_data: dict) -> PayoutAdjustmentEntity:
        adjustment = get_object_or_404(PayoutAdjustment, id=adjustment_id)

        for key, value in update_data.items():
            setattr(adjustment, key, value)

        adjustment.save()
        return self._to_entity(adjustment)

    def delete(self, adjustment_id: int) -> None:
        adjustment = get_object_or_404(PayoutAdjustment, id=adjustment_id)
        adjustment.delete()