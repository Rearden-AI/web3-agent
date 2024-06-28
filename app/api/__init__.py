from fastapi import APIRouter

# from .stats.views import router as dashboard_router
# from .transactions.views import router as transactions_router
# from .users.views import router as users_router
from .auth.views import router as auth_router
from .chats.views import router as chats_router
from .transactions.views import router as transactions_router
from .strategy_executions.views import router as strategy_executions_router

router = APIRouter()

# router.include_router(router=users_router, prefix="/users")
router.include_router(router=auth_router, prefix="/auth")
router.include_router(router=chats_router, prefix="/chats")
router.include_router(router=transactions_router, prefix="/transactions")
router.include_router(router=strategy_executions_router, prefix="/strategy_executions")
# router.include_router(router=projects_router, prefix="/projects")
# router.include_router(router=dashboard_router, prefix="/dashboard")
