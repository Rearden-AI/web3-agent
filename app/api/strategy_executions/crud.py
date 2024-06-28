from datetime import datetime

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.strategy_executions.schemas import StrategyExecutionCreate
from app.core.models import StrategyExecution


async def create_strategy_execution(
        session: AsyncSession,
        strategy_execution_in: StrategyExecutionCreate
) -> StrategyExecution:
    strategy_execution = StrategyExecution(
        created_at=datetime.now(),
        **strategy_execution_in.model_dump()
    )
    print(strategy_execution.created_at)
    session.add(strategy_execution)
    await session.commit()

    return strategy_execution


async def get_strategy_executions(
    session: AsyncSession,
) -> list[StrategyExecution]:
    stmt = select(StrategyExecution)
    result: Result = await session.execute(stmt)
    strategy_executions = result.scalars().all()
    return list(strategy_executions)
