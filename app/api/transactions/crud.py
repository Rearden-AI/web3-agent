import datetime
import logging
import time

from fastapi_sa_orm_filter.main import FilterCore
from fastapi_sa_orm_filter.operators import Operators as ops
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Transaction
from app.core.modules_factory import web3
from utils.paginated_response import paginate, PaginatedParams, PaginatedResponse
from .schemas import TransactionSchema, TransactionExtended, TransactionCreate, TransactionUpdate

transaction_query_filters = {
    'created_at': [ops.gte, ops.lte, ops.eq],
    'updated_at': [ops.gte, ops.lte, ops.eq],
    'name': [ops.like, ops.ilike],
    'user_id': [ops.eq]
}


async def get_all(
        session: AsyncSession, filter_query: str, pagination_query: PaginatedParams
) -> PaginatedResponse[TransactionSchema]:
    filter_inst = TransactionFilter(Transaction, transaction_query_filters)
    stmt = filter_inst.get_query(filter_query)
    response, data = await paginate(
        session=session, query=stmt,
        page_size=pagination_query.page_size, page_number=pagination_query.page_number
    )

    res = []
    for transaction in data:
        r = TransactionExtended.model_validate(
            {
                **vars(transaction),
            })
        res.append(r)
    response["data"] = res

    return response


async def get_all_users_transactions(
        session: AsyncSession, filter_query: str,
        pagination_query: PaginatedParams
) -> PaginatedResponse[TransactionSchema]:
    filter_inst = UserTransactionFilter(Transaction, transaction_query_filters)
    stmt = filter_inst.get_query(filter_query)

    response, data = await paginate(
        session=session, query=stmt,
        page_size=pagination_query.page_size, page_number=pagination_query.page_number
    )

    res = []
    for transaction in data:
        _d = {**vars(transaction), "user": vars(transaction.user)}
        r = TransactionSchema(**_d)
        res.append(r)
    response["data"] = res

    return response


async def create(session: AsyncSession, transaction_in: TransactionCreate) -> Transaction | None:
    transaction = Transaction(
        # created_at=int(time.time()),
        # updated_at=int(time.time()),
        **transaction_in.model_dump(),
    )
    session.add(transaction)
    await session.commit()
    return transaction


async def get_by_id(session: AsyncSession, transaction_id: int) -> Transaction | None:
    stmt = (
        select(Transaction)
        .filter(Transaction.id == transaction_id)
    )
    result: Result = await session.execute(stmt)
    transaction = result.scalars().first()
    return transaction


async def update_transactions_status(
        session: AsyncSession,
) -> dict:
    logging.info("Transactions status check running!")
    stmt = select(Transaction).filter(Transaction.status == "pending")
    query: Result = await session.execute(stmt)
    transactions = query.scalars().all()
    for t in transactions:
        receipt = web3.eth.get_transaction_receipt(t.transaction_hash)
        if receipt['status'] == 1:
            t.status = "succeeded"
        elif receipt['status'] == 0:
            t.status = "failed"
        t.updated_at = int(time.time())
        await session.commit()
    return {"ok": True}


async def get_transactions_by_chat_uuid(session: AsyncSession, chat_uuid: str):
    stmt = select(Transaction).filter(Transaction.chat_uuid == chat_uuid)
    query: Result = await session.execute(stmt)
    transactions = query.scalars().all()
    response = []
    for t in transactions:
        response.append(TransactionSchema.model_validate({**vars(t)}))
    return response

async def update_transaction(
    session: AsyncSession, 
    transaction: Transaction,
    transaction_update: TransactionUpdate
):
    for name, value in transaction_update.model_dump().items():
        setattr(transaction, name, value)
    await session.commit()
    return transaction
    
    
class TransactionFilter(FilterCore):

    def get_select_query_part(self):
        return (
            select(Transaction)
        )


class UserTransactionFilter(FilterCore):

    def get_select_query_part(self):
        return (
            select(Transaction)
        )
