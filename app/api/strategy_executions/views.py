from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from . import crud
from .schemas import StrategyExecutionCreate, StrategyExecution

router = APIRouter(tags=["StrategyExecutions"])


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=StrategyExecution
)
async def create_new_strategy_execution(
    strategy_execution_in: StrategyExecutionCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_strategy_execution(session=session, strategy_execution_in=strategy_execution_in)


@router.get(
    path="",
    response_model=list[StrategyExecution]
)
async def get_strategy_executions(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_strategy_executions(session=session)
