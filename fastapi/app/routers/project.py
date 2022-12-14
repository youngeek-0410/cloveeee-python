import time

from app.api import ProjectAPI
from app.models import Project
from app.schemas import (
    CreateProjectSchema,
    ReadProjectSchema,
    CreateProjectTopTextSchema,
    CreateProjectTopImageSchema,
    SpotifyMusicSchema,
    AllProjectsIdSchema,
)

from fastapi import APIRouter, Request, Response

project_router = APIRouter()
spotify_music_router = APIRouter()


@project_router.get("/{project_id}", response_model=ReadProjectSchema)
async def get(
    request: Request,
    project_id: str,
    text_message_limit: int = 100,
    image_messages_limit: int = 100,
) -> Project:
    return await ProjectAPI.get(
        request, project_id, text_message_limit, image_messages_limit
    )


@project_router.put("/{project_id}/top_text", response_class=Response)
async def create_top_text(
        request: Request,
        project_id: str,
        schema: CreateProjectTopTextSchema,
) -> None:
    await ProjectAPI.put_top_text(request, project_id, schema)


@project_router.put("/{project_id}/top_image", response_class=Response)
async def create_top_image(
        request: Request,
        project_id: str,
        schema: CreateProjectTopImageSchema,
) -> None:
    await ProjectAPI.put_top_image(request, project_id, schema)


@spotify_music_router.put(
    "/{project_id}/spotify_music",
    response_class=Response,
)
async def create_spotify_music(
        request: Request,
        project_id: str,
        schema: SpotifyMusicSchema,
) -> None:
    await ProjectAPI.put_spotify_uri(request, project_id, schema)


@project_router.post(
    "/",
    response_model=ReadProjectSchema,
    response_model_exclude_none=True,
)
async def create(request: Request, schema: CreateProjectSchema) -> Project:
    return await ProjectAPI.create(request, schema)


@project_router.get(
    "/all_id/",
    response_model=AllProjectsIdSchema,
)
async def get(request: Request) -> list:
    return await ProjectAPI.get_all_project_id(request)
