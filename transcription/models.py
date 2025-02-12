from django.db import models

class Transcription(models.Model):
    audio_file = models.FileField(upload_to="audio/")
    text = models.TextField()
    duration = models.FloatField(blank=True, null=True)
    segments = models.JSONField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)