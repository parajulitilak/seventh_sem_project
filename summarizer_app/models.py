# summarizer_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    input_text = models.TextField()
    algorithm = models.CharField(max_length=50)
    summary_length = models.IntegerField()
    summarized_text = models.TextField(blank=True)  # Rename generated_summary to summarized_text
    short_topic = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'


