from rest_framework.serializers import ValidationError
from urllib.parse import urlparse

def validate_video_url(video_url):
    parsed_url = urlparse(video_url)
    if parsed_url.netloc not in ["www.youtube.com", "youtube.com"]:
        raise ValidationError("Нужно использовать только ссылки на YouTube.")
