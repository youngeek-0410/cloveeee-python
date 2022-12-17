import random
from logging import getLogger

from app.models import Project
from app.schemas import (
    CreateProjectSchema,
    CreateProjectTopTextSchema,
    CreateProjectTopImageSchema,
    SpotifyMusicSchema,
    PublicationUrlSchema,
)
from asgiref.sync import sync_to_async
from config.exceptions import NotFoundException

from fastapi import Request, HTTPException

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

        project.top_image_url = schema.top_image_url
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

    @classmethod
    async def get_all_project_id(cls, request: Request) -> list:
        return [project.id for project in Project.objects.all()]

    @classmethod
    async def post_publication_url(cls, request: Request, project_id: str) -> bool:
        project = await Project.objects.filter(id=project_id).afirst()
        if not project:
            raise NotFoundException("Project not found")

        text_message_count = await project.get_text_message_count()
        image_message_count = await project.get_image_message_count()

        # Ensure that the project meets the minimum requirements for publication
        if (project.top_text and
                project.top_image_url and
                project.spotify_uri and
                text_message_count >= 5 and
                image_message_count >= 5):
            project.is_publish = True
        else:
            project.is_publish = False
            raise HTTPException(status_code=400,
                                detail="Does not meet the requirements to publish the project.",
                                )
        await sync_to_async(project.save)()
