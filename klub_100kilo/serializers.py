from rest_framework import serializers
from .models import Reservations


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ["user", "type", "status", "gym", "trainer_id", "date"]
