import json
import logging
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status, Form, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import errors
from app.core.models import db_helper, Transaction
from utils.paginated_response import PaginatedParams, PaginatedResponse
from . import crud
from .schemas import TransactionSchema, TransactionCreate


async def get_all_transactions(
        objects_filter: str = Query(default=''),
        pagination_query: PaginatedParams = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> PaginatedResponse[TransactionSchema]:
    res = await crud.get_all(session=session, filter_query=objects_filter, pagination_query=pagination_query)
    return res


async def get_transaction_by_id(
        transaction_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Transaction:
    transaction = await crud.get_by_id(session=session, transaction_id=transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=errors.transactions.TRANSACTION_NOT_FOUND
        )

    return transaction


async def get_transaction_by_chat_uuid(
        chat_uuid: Annotated[str, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    transactions = await crud.get_transactions_by_chat_uuid(session=session, chat_uuid=chat_uuid)
    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=errors.transactions.TRANSACTION_NOT_FOUND
        )

    return transactions


async def process_transaction_to_create(
        transaction_in: TransactionCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Transaction:
    try:
        transaction = await crud.create(session=session, transaction_in=transaction_in)
    except IntegrityError:
        await session.rollback()
        await session.close()
        logging.error(errors.transactions.TRANSACTION_HASH_NOT_UNIQUE)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=errors.transactions.TRANSACTION_HASH_NOT_UNIQUE
        )
    logging.debug(f"Transaction created: {transaction}")
    await session.commit()

    return transaction


async def check_transactions_for_update(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    result = await crud.update_transactions_status(
        session=session
    )

    return result
