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
        Register availability for a candidate or interviewer

        Example POST data:
        {
            "user_id": "123",
            "user_type": "CANDIDATE",
            "start_time": "2024-02-05T10:00:00",
            "end_time": "2024-02-05T14:00:00"
        }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def check_overlap(self, request):
        """
        Check overlapping available time slots between candidate and interviewer
        """
        serializer = OverlapCheckSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Base filters
        candidate_filter = {
            'user_id': data['candidate_id'],
            'user_type': 'CANDIDATE'
        }

        interviewer_filter = {
            'user_id': data['interviewer_id'],
            'user_type': 'INTERVIEWER'
        }

        # Add date filter if provided
        if 'date' in data:
            start_of_day = datetime.combine(data['date'], datetime.min.time())
            end_of_day = datetime.combine(data['date'], datetime.max.time())
            candidate_filter['start_time__date'] = data['date']
            interviewer_filter['start_time__date'] = data['date']

        # Get time slots with logging
        candidate_slots = TimeSlot.objects.filter(**candidate_filter)
        interviewer_slots = TimeSlot.objects.filter(**interviewer_filter)

        # Debug logging
        print(f"Candidate filter: {candidate_filter}")
        print(f"Interviewer filter: {interviewer_filter}")
        print(f"Found {candidate_slots.count()} candidate slots")
        print(f"Found {interviewer_slots.count()} interviewer slots")

        # Find overlapping slots
        available_slots = []
        for c_slot in candidate_slots:
            print(f"\nCandidate slot: {c_slot.start_time} - {c_slot.end_time}")
            for i_slot in interviewer_slots:
                print(f"Checking against interviewer slot: {i_slot.start_time} - {i_slot.end_time}")
                # Find overlap
                start = max(c_slot.start_time, i_slot.start_time)
                end = min(c_slot.end_time, i_slot.end_time)

                print(f"Potential overlap: {start} - {end}")

                if start < end:
                    print("Found overlap!")
                    # Generate 1-hour slots within overlap
                    current = start
                    while current + timedelta(hours=1) <= end:
                        available_slots.append({
                            'date': current.date().strftime('%Y-%m-%d'),
                            'start_time': current.strftime('%H:%M'),
                            'end_time': (current + timedelta(hours=1)).strftime('%H:%M')
                        })
                        current += timedelta(hours=1)

        response_data = {
            'overlapping_slots': available_slots,
            'debug_info': {
                'candidate_slots_count': candidate_slots.count(),
                'interviewer_slots_count': interviewer_slots.count(),
                'candidate_slots': [{
                    'start': slot.start_time,
                    'end': slot.end_time
                } for slot in candidate_slots],
                'interviewer_slots': [{
                    'start': slot.start_time,
                    'end': slot.end_time
                } for slot in interviewer_slots]
            },
            'availability_summary': {
                'candidate': [{
                    'date': slot.start_time.date().strftime('%Y-%m-%d'),
                    'start_time': slot.start_time.strftime('%H:%M'),
                    'end_time': slot.end_time.strftime('%H:%M')
                } for slot in candidate_slots],
                'interviewer': [{
                    'date': slot.start_time.date().strftime('%Y-%m-%d'),
                    'start_time': slot.start_time.strftime('%H:%M'),
                    'end_time': slot.end_time.strftime('%H:%M')
                } for slot in interviewer_slots]
            }
        }

        return Response(response_data)