# import whisper
# import tempfile
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from transcription.models import Transcription
# from .serializers import TranscriptionSerializer

# class SpeechToTextViewSet(viewsets.ModelViewSet):
#     queryset = Transcription.objects.all()
#     serializer_class = TranscriptionSerializer
#     parser_classes = (MultiPartParser, FormParser)

#     def create(self, request, *args, **kwargs):
#         audio_file = request.FILES.get('audio_file')
#         if not audio_file:
#             return Response({"error": "Audio file is required."}, status=status.HTTP_400_BAD_REQUEST)

#         model = whisper.load_model("small")  

#         try:
#             with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.name.split('.')[-1]}") as temp_audio:
#                 temp_audio.write(audio_file.read())
#                 temp_audio_path = temp_audio.name 

#             result = model.transcribe(temp_audio_path)
#             transcription_text = result['text']

#             transcription = Transcription.objects.create(
#                 audio_file=audio_file,
#                 text=transcription_text
#             )
#             serializer = self.get_serializer(transcription)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import whisper
import tempfile
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from pydub.utils import mediainfo
from transcription.models import Transcription
from .serializers import TranscriptionSerializer

class SpeechToTextViewSet(viewsets.ModelViewSet):
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        audio_file = request.FILES.get('audio_file')
        if not audio_file:
            return Response({"error": "Audio file is required."}, status=status.HTTP_400_BAD_REQUEST)

        model = whisper.load_model("small")  # or "base", "large", depending on your needs

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.name.split('.')[-1]}") as temp_audio:
                temp_audio.write(audio_file.read())
                temp_audio_path = temp_audio.name 

            # Calculate the duration of the audio file using pydub or ffmpeg
            audio_info = mediainfo(temp_audio_path)
            audio_duration = float(audio_info['duration'])  # Duration in seconds

            # Perform transcription with timestamps
            result = model.transcribe(temp_audio_path, word_timestamps=True)
            segments = result['segments']  # List of segments with text and timestamps

            # Prepare segments for storage as a JSON list
            segment_data = []
            for segment in segments:
                segment_duration = segment['end'] - segment['start']  # Calculate duration of each segment
                segment_data.append({
                    'start_time': segment['start'],
                    'end_time': segment['end'],
                    'duration': segment_duration,  # Duration of the segment
                    'text': segment['text']
                })

            # Create a transcription object and store the total duration and segments
            transcription = Transcription.objects.create(
                audio_file=audio_file,
                text=result['text'],
                duration=audio_duration,  # Store total duration of the audio file
                segments=segment_data  # Store segments in JSON format
            )

            # Serialize and return the result
            serializer = self.get_serializer(transcription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
