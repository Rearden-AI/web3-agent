# pylint: disable=raise-missing-from
import pickle
import logging
from fastapi import APIRouter, Body, Cookie, HTTPException, Response, status, Depends, Request
from fastapi.responses import PlainTextResponse
from siwe import generate_nonce, SiweMessage

from app.core.modules_factory import redis_db
from app.api.auth.utils import generate_session_id
from app.core.models import User

from . import dependencies
from .constants import COOKIE_SESSION_ID_KEY

logger = logging.getLogger("auth/views")

router = APIRouter(
    tags=["Authorization"],
    responses={404: {"description": "Not found"}},
)


@router.get(
        "/nonce",
        response_class=PlainTextResponse
)
async def get_nonce(
    response: Response,
    request: Request
):
    logger.info('Received /nonce')
    logger.debug("IP: %s", request.client.host)
    logger.debug("Platform: %s", request.headers.get("sec-ch-ua-platform"))
    logger.debug("Browser: %s", request.headers.get("sec-ch-ua"))
    try:
        session_id = generate_session_id()

        nonce = generate_nonce()
        session_info = {
            'nonce': nonce
        }
        redis_db.set(session_id, pickle.dumps(session_info))

        response.set_cookie(
            key=COOKIE_SESSION_ID_KEY,
            value=session_id,
            samesite='none',
            secure=True)

        logger.debug("Return nonce %s. Session id: %s", nonce, session_id)

        return nonce
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
    logger.info("Got verify. Session id: %s", session_id)
    try:
        siwe_message = SiweMessage.from_message(message)

        session_info = pickle.loads(redis_db.get(session_id))
        siwe_message.verify(
            signature=signature,
            nonce=session_info['nonce']
        )

        session_info['siwe'] = siwe_message
        redis_db.set(session_id, pickle.dumps(session_info))
        # COOKIES[session_id]['expires'] = int(time.time())

        logger.debug("Verified successfully. Session id: %s", session_id)

        return True
    except:
        logger.exception("Failed to verify. Session id: %s", session_id)

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


@router.post("/logout")
async def logout(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)
):
    logger.info("Received logout. Session id: %s", session_id)
    try:
        redis_db.delete(session_id)

        logger.debug("Successfully logged out. Session id: %s", session_id)
    except Exception:
        logger.exception("Failed to logout. Session id: %s", session_id)


@router.get("/me")
async def me(
    user: User = Depends(dependencies.extract_user_from_access_token),
):
    logger.info("Gout /me. Wallet %s", user.wallet)
    return user.wallet
