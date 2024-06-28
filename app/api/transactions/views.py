from fastapi import APIRouter, status, Depends
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper, User, Transaction
from utils.paginated_response import PaginatedResponse, PaginatedParams
from .schemas import TransactionCreate, TransactionSchema, TransactionExtended, TransactionUpdate
from . import crud
from . import dependencies

router = APIRouter(tags=["Transactions"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[TransactionExtended],
)
async def get_all_transactions(
        objects_filter: str = Query(default=''),
        pagination_query: PaginatedParams = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    res = await crud.get_all(session=session, filter_query=objects_filter, pagination_query=pagination_query)
    return res


@router.post(
    "",
    response_model=TransactionExtended,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
        transaction: TransactionCreate = Depends(dependencies.process_transaction_to_create),
):
    res = TransactionExtended.model_validate(transaction)
    return res


@router.get(
    "/{transaction_id}",
    status_code=status.HTTP_200_OK,
    response_model=TransactionExtended,
)
async def get_selected_transaction(
        transaction: Transaction = Depends(dependencies.get_transaction_by_id),
):
    res = TransactionExtended.model_validate(transaction)
    return res


@router.post(
    "/check",
    status_code=status.HTTP_200_OK,
)
async def check_transactions_status(
        res: dict = Depends(dependencies.check_transactions_for_update),
):
    return res


@router.get(
    "/chat/{chat_uuid}",
    status_code=status.HTTP_200_OK,
    response_model=list[TransactionSchema],
)
async def get_transactions(
        transactions: list[TransactionSchema] = Depends(dependencies.get_transaction_by_chat_uuid),
):
    return transactions

@router.patch(
    "/{transaction_id}",
    response_model=TransactionExtended
)
async def update_transaction(
    transaction_update: TransactionUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    transaction: Transaction = Depends(dependencies.get_transaction_by_id)  
):
    return await crud.update_transaction(
        session=session,
        transaction=transaction,
        transaction_update=transaction_update
    )