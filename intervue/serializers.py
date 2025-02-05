from rest_framework import serializers
from .models import TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'user_id', 'user_type', 'start_time', 'end_time']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time")
        return data

class OverlapCheckSerializer(serializers.Serializer):
    candidate_id = serializers.CharField()
    interviewer_id = serializers.CharField()
    date = serializers.DateField(required=False)