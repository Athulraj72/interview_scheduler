from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
from .models import TimeSlot
from .serializers import TimeSlotSerializer, OverlapCheckSerializer


class InterviewSchedulerViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer

    def create(self, request):
        """
        Create a new time slot.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def check_overlap(self, request):
        """
        Check overlapping time slots between a candidate and an interviewer.
        """
        serializer = OverlapCheckSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Filter criteria
        candidate_slots = TimeSlot.objects.filter(
            user_id=data['candidate_id'], user_type='CANDIDATE'
        )
        interviewer_slots = TimeSlot.objects.filter(
            user_id=data['interviewer_id'], user_type='INTERVIEWER'
        )

        if 'date' in data:
            candidate_slots = candidate_slots.filter(start_time__date=data['date'])
            interviewer_slots = interviewer_slots.filter(start_time__date=data['date'])

        # Find overlapping time slots
        available_slots = []
        for c_slot in candidate_slots:
            for i_slot in interviewer_slots:
                start, end = max(c_slot.start_time, i_slot.start_time), min(c_slot.end_time, i_slot.end_time)

                if start < end:  # Valid overlap
                    current = start
                    while current + timedelta(hours=1) <= end:
                        available_slots.append({
                            'date': current.date().strftime('%Y-%m-%d'),
                            'start_time': current.strftime('%H:%M'),
                            'end_time': (current + timedelta(hours=1)).strftime('%H:%M')
                        })
                        current += timedelta(hours=1)

        return Response({'overlapping_slots': available_slots}, status=status.HTTP_200_OK)
