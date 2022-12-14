import random

from django.db import models

from .base import TimestampModelMixin
from .message import Message, MessageImage


def get_default_spotify_uri() -> str:
    spotify_uri_candidates = [
        "spotify:album:6uqewERWZ1vzfCcin1zFIp",
    ]
    return random.choice(spotify_uri_candidates)


class Project(TimestampModelMixin):
    MAX_LENGTH_ID = 32
    DEFAULT_LENGTH_ID = 7
    id = models.CharField(max_length=MAX_LENGTH_ID, primary_key=True, editable=False)

    MAX_LENGTH_RECEIVER_NAME = 32
    receiver_name = models.CharField(max_length=MAX_LENGTH_RECEIVER_NAME)

    MAX_LENGTH_TOP_TEXT = 32
    top_text = models.CharField(max_length=MAX_LENGTH_TOP_TEXT, default="")

    MAX_LENGTH_URL = 256
    top_image_url = models.URLField(max_length=MAX_LENGTH_URL, default="")

    MAX_LENGTH_URI = 256
    spotify_uri = models.CharField(
        default=get_default_spotify_uri, max_length=MAX_LENGTH_URI
    )

    def __str__(self) -> str:
        return f"Project for {self.receiver_name} [{self.id}]"

    async def get_text_messages(self, limit: int) -> list["Message"]:
        return [
            obj
            async for obj in Message.objects.filter(project=self)
            .order_by("-created_at")
            .all()
        ][:limit]

    async def get_image_messages(self, limit: int) -> list["MessageImage"]:
        return [
            obj
            async for obj in MessageImage.objects.filter(message__project=self)
            .order_by("-created_at")
            .all()
        ][:limit]
