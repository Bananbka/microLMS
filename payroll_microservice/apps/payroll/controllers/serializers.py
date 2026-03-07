from rest_framework import serializers


### ADJUSTMENTS
class PayoutAdjustmentResponseDTO(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    category = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payout_id = serializers.IntegerField(allow_null=True)
    created_at = serializers.DateTimeField()


class PayoutAdjustmentCreateUpdateDTO(serializers.Serializer):
    user = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    category = serializers.CharField(max_length=50, required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    payout_id = serializers.IntegerField(required=False, allow_null=True)


### PAYOUTS
class PayoutResponseDTO(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    status = serializers.CharField()
    created_at = serializers.DateTimeField()

    adjustments = PayoutAdjustmentResponseDTO(many=True, read_only=True)


class PayoutCreateUpdateDTO(serializers.Serializer):
    user = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    status = serializers.CharField(max_length=50, required=False)