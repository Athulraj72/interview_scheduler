from django.db import models


class TimeSlot(models.Model):
    USER_TYPES = (
        ('CANDIDATE', 'Candidate'),
        ('INTERVIEWER', 'Interviewer')
    )

    user_id = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'user_type']),
        ]