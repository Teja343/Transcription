from rest_framework.routers import DefaultRouter
from .views import SpeechToTextViewSet

router = DefaultRouter()
router.register(r'transcriptions', SpeechToTextViewSet, basename='transcription')

urlpatterns = router.urls
