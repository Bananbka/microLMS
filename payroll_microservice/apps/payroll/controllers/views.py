from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from core.permissions import HasPermission

from .serializers import (
    PayoutResponseDTO, PayoutCreateUpdateDTO,
    PayoutAdjustmentResponseDTO, PayoutAdjustmentCreateUpdateDTO
)
from ..services.adjustment_service import PayoutAdjustmentService
from ..services.payout_service import PayoutService


### PAYOUT
class PayoutListCreateAPIView(APIView):
    permission_classes = [HasPermission]
    required_permissions = ['payroll.manage']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payout_service = PayoutService()

    @extend_schema(tags=["Payroll/Payouts"], responses=PayoutResponseDTO(many=True))
    def get(self, request):
        payouts = self.payout_service.get_all_payouts()
        output_dto = PayoutResponseDTO(payouts, many=True)
        return Response(output_dto.data)

    @extend_schema(tags=["Payroll/Payouts"], request=PayoutCreateUpdateDTO, responses=PayoutResponseDTO)
    def post(self, request):
        input_dto = PayoutCreateUpdateDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)

        payout = self.payout_service.create_payout(input_dto.validated_data)
        output_dto = PayoutResponseDTO(payout)
        return Response(output_dto.data, status=201)


class PayoutDetailAPIView(APIView):
    permission_classes = [HasPermission]
    required_permissions = ['payroll.manage']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payout_service = PayoutService()

    @extend_schema(tags=["Payroll/Payouts"], responses=PayoutResponseDTO)
    def get(self, request, payout_id):
        payout = self.payout_service.get_payout(payout_id)
        output_dto = PayoutResponseDTO(payout)
        return Response(output_dto.data)

    @extend_schema(tags=["Payroll/Payouts"], request=PayoutCreateUpdateDTO, responses=PayoutResponseDTO)
    def patch(self, request, payout_id):
        input_dto = PayoutCreateUpdateDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)

        payout = self.payout_service.update_payout(payout_id, input_dto.validated_data)
        output_dto = PayoutResponseDTO(payout)
        return Response(output_dto.data)

    @extend_schema(tags=["Payroll/Payouts"], responses={204: None})
    def delete(self, request, payout_id):
        self.payout_service.delete_payout(payout_id)
        return Response(status=204)


### PAYOUT ADJUSTMENTS
class AdjustmentListCreateAPIView(APIView):
    permission_classes = [HasPermission]
    required_permissions = ['payroll.manage']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.adjustment_service = PayoutAdjustmentService()

    @extend_schema(tags=["Payroll/Adjustments"], responses=PayoutAdjustmentResponseDTO(many=True))
    def get(self, request):
        adjustments = self.adjustment_service.get_all_adjustments()
        output_dto = PayoutAdjustmentResponseDTO(adjustments, many=True)
        return Response(output_dto.data)

    @extend_schema(tags=["Payroll/Adjustments"], request=PayoutAdjustmentCreateUpdateDTO,
                   responses=PayoutAdjustmentResponseDTO)
    def post(self, request):
        input_dto = PayoutAdjustmentCreateUpdateDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)

        adjustment = self.adjustment_service.create_adjustment(input_dto.validated_data)
        output_dto = PayoutAdjustmentResponseDTO(adjustment)
        return Response(output_dto.data, status=201)


class AdjustmentDetailAPIView(APIView):
    permission_classes = [HasPermission]
    required_permissions = ['payroll.manage']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.adjustment_service = PayoutAdjustmentService()

    @extend_schema(tags=["Payroll/Adjustments"], responses=PayoutAdjustmentResponseDTO)
    def get(self, request, adjustment_id):
        adjustment = self.adjustment_service.get_adjustment(adjustment_id)
        output_dto = PayoutAdjustmentResponseDTO(adjustment)
        return Response(output_dto.data)

    @extend_schema(tags=["Payroll/Adjustments"], request=PayoutAdjustmentCreateUpdateDTO,
                   responses=PayoutAdjustmentResponseDTO)
    def patch(self, request, adjustment_id):
        input_dto = PayoutAdjustmentCreateUpdateDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)

        adjustment = self.adjustment_service.update_adjustment(adjustment_id, input_dto.validated_data)
        output_dto = PayoutAdjustmentResponseDTO(adjustment)
        return Response(output_dto.data)

    @extend_schema(tags=["Payroll/Adjustments"], responses={204: None})
    def delete(self, request, adjustment_id):
        self.adjustment_service.delete_adjustment(adjustment_id)
        return Response(status=204)
