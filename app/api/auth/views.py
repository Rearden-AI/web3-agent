# pylint: disable=raise-missing-from
import logging
from typing import Any
from fastapi import APIRouter, Body, Cookie, HTTPException, Response, status
from fastapi.responses import PlainTextResponse
from siwe import generate_nonce, SiweMessage

from app.api.auth.utils import generate_session_id

logger = logging.getLogger("auth/views")

router = APIRouter(
    tags=["Authorization"],
    responses={404: {"description": "Not found"}},
)

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "rearden-session-id"


@router.get(
        "/nonce",
        response_class=PlainTextResponse
)
async def get_nonce(
    response: Response
):
    logger.info('Received /nonce')
    try:
        session_id = generate_session_id()

        COOKIES[session_id] = {
            'nonce': generate_nonce()
        }

        response.set_cookie(
            key=COOKIE_SESSION_ID_KEY,
            value=session_id,
            samesite='none',
            secure=True)

        return COOKIES[session_id]['nonce']
    except Exception as e:
        logger.error(e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate nonce"
        )


@router.post('/verify')
def verify(
        message: str = Body(),
        signature: str = Body(),
        session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)
):
    try:
        siwe_message = SiweMessage.from_message(message)
        siwe_message.verify(
            signature=signature,
            nonce=COOKIES[session_id]['nonce']
        )

        COOKIES[session_id]['siwe'] = siwe_message
        COOKIES[session_id]['expires'] = siwe_message.expiration_time

        return True
    except Exception as e:
        print(e)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Wrong credentials {session_id}",
        )


# @router.post("/refresh")
# async def refresh_token(token: str) -> TokenResponse:
#     pass
    # try:
    #     auth = credentials_manager.refresh_token(token)
    # except TimeoutError as e:
    #     raise HTTPException(401, "Token expired") from e
    # except NotAuthorizedError as e:
    #     raise HTTPException(401, "Not authorized") from e
    # return TokenResponse(
    #     address=auth.address,
    #     chain=auth.chain,
    #     token=auth.token,
    #     valid_til=auth.valid_til,
    # )
