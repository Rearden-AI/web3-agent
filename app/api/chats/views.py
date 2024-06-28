from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import dependencies as auth_dependencies
from app.core.models import db_helper, Chat
from utils.paginated_response import PaginatedResponse, PaginatedParams
from . import crud
from . import dependencies
from .schemas import ChatSchema, ExtendedChatSchema, ChatUpdatePartial

router = APIRouter(tags=["Chats"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[ChatSchema],
)
async def get_all_chats(
        user=Depends(auth_dependencies.extract_user_from_access_token),
        pagination_query: PaginatedParams = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    res = await crud.get_all(session=session, pagination_query=pagination_query, user_id=user.id)
    return res


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(RateLimiter(times=1, seconds=1))],
    # response_model=ChatSchema,
)
async def create_new_chat(
        chat: ChatSchema = Depends(dependencies.start_new_chat),
):
    return chat


@router.get(
    "/{chat_uuid}",
    status_code=status.HTTP_200_OK,
    response_model=ExtendedChatSchema,
)
async def get_selected_chat(
    chat: ExtendedChatSchema = Depends(dependencies.get_extended_chat_by_uuid),
):
    return chat


@router.post(
    "/{chat_uuid}",
    # dependencies=[Depends(RateLimiter(times=1, seconds=10))],
    status_code=status.HTTP_200_OK,
)
async def start_chat_streaming(
        chat: ChatSchema = Depends(dependencies.process_chat_request),
):
    return chat


@router.post(
    "/{chat_uuid}/demo",
    # dependencies=[Depends(RateLimiter(times=1, seconds=10))],
    status_code=status.HTTP_200_OK,
    # response_model=ChatResponse
)
async def demo_chat(
        response=Depends(dependencies.process_chat_request)
):
    return response


@router.delete(
    "/{chat_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_selected_chat(
    chat: Chat = Depends(dependencies.get_chat_by_uuid),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_chat(session, chat)


@router.patch("/{chat_uuid}")
async def patch_selected_chat(
    chat_update: ChatUpdatePartial,
    chat: Chat = Depends(dependencies.get_chat_by_uuid),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_chat(
        session=session,
        chat=chat,
        chat_update=chat_update,
        partial=True
    )
