from rest_framework import serializers
from transcription.models import Transcription

class TranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcription
        fields = ['id', 'audio_file', 'text', 'duration', 'segments']