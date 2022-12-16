import base64
import binascii
import random
import io
from PIL import Image
import numpy as np
from logging import getLogger

from app.models import Project
from app.schemas import (
    CreateProjectSchema,
    CreateProjectTopTextSchema,
    CreateProjectTopImageSchema,
    SpotifyMusicSchema,
)
from asgiref.sync import sync_to_async
from config.exceptions import NotFoundException, BadRequestException
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from fastapi import Request

logger = getLogger(__name__)


# FIXME: 使用する頻度に応じて別ファイルに切り出し
def generate_base58_id(length: int) -> str:
    base58_strings = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
    return "".join(random.choice(base58_strings) for _ in range(length))


class ProjectAPI:
    @classmethod
    async def get(
            cls,
            request: Request,
            id: str,
            text_messages_limit: int,
            image_messages_limit: int,
    ) -> Project:
        project = await Project.objects.filter(id=id).afirst()
        if not project:
            raise NotFoundException("Project not found.")

        # FIXME: @propertyを使って出来たら嬉しい
        setattr(
            project,
            "text_messages",
            await project.get_text_messages(text_messages_limit),
        )
        setattr(
            project,
            "image_messages",
            await project.get_image_messages(image_messages_limit),
        )
        return project

    @classmethod
    async def put_top_text(
            cls,
            request: Request,
            id: str,
            schema: CreateProjectTopTextSchema,
    ) -> None:
        project = await Project.objects.filter(id=id).afirst()
        if not project:
            raise NotFoundException("Project not found.")

        project.top_text = schema.top_text
        await sync_to_async(project.save)()

    @classmethod
    async def put_top_image(
            cls,
            request: Request,
            id: str,
            schema: CreateProjectTopImageSchema,
    ) -> None:
        project = await Project.objects.filter(id=id).afirst()
        if not project:
            raise NotFoundException("Project not found.")

        try:
            image_binary = base64.b64decode(schema.image)
        except binascii.Error:
            raise BadRequestException("Invalid base64 string")

        jpg = np.frombuffer(image_binary, dtype=np.uint8)
        image = Image.fromarray(jpg).convert('RGB')
        image_io = io.BytesIO()
        image_name = "top_image.jpg"
        # TODO: saveするときにエラー出るから直したい
        image.save(image_io, format="JPEG")
        image_file = InMemoryUploadedFile(image_io, field_name=None, name=image_name,
                                          content_type="image/jpeg", size=image_io.getbuffer().nbytes,
                                          charset=None)
        project.top_image = image_file
        await sync_to_async(project.save)()

    @classmethod
    async def put_spotify_uri(
            cls,
            request: Request,
            id: str,
            schema: SpotifyMusicSchema,
    ) -> None:
        project = await Project.objects.filter(id=id).afirst()
        if not project:
            raise NotFoundException("Project not found.")

        project.spotify_uri = schema.uri
        await sync_to_async(project.save)()

    @classmethod
    async def create(cls, request: Request, schema: CreateProjectSchema) -> Project:
        project = await sync_to_async(Project.objects.create)(
            **schema.dict(), id=generate_base58_id(Project.DEFAULT_LENGTH_ID)
        )
        return project
