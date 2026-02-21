from django.urls import path
from .views import PayoutListCreateAPIView, PayoutDetailAPIView, AdjustmentListCreateAPIView, AdjustmentDetailAPIView

urlpatterns = [
    path('payouts/', PayoutListCreateAPIView.as_view(), name='payout-list-create'),
    path('payouts/<int:payout_id>/', PayoutDetailAPIView.as_view(), name='payout-detail'),

    path('adjustments/', AdjustmentListCreateAPIView.as_view(), name='adjustment-list-create'),
    path('adjustments/<int:adjustment_id>/', AdjustmentDetailAPIView.as_view(), name='adjustment-detail'),
]
