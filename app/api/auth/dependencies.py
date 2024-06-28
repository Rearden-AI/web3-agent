from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper, User
from . import crud
from .views import COOKIE_SESSION_ID_KEY, COOKIES


async def extract_user_from_access_token(
        session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY, default='ddd'),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    if not COOKIES.get(session_id) or not COOKIES[session_id].get('siwe'):
        # return await crud.select_by_wallet(
        #     session=session,
        #     wallet='0x5D8fdccF4Bd9B1331e66Ff2606457fbc876F28de')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have to first sign_in",
        )

    address = COOKIES[session_id]['siwe'].address


    user = await crud.select_by_wallet(session=session, wallet=address)
    if not user:
        # logging.warning(f"Not found user by wallet: {address}")
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        user = await crud.add_user(session=session, wallet=address)
    return user
