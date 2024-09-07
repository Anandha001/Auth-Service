from fastapi import APIRouter

from resources.auth_controller import router as auth_router
from resources.member_controller import router as member_router
from resources.stat_controller import router as stat_router


router = APIRouter()


router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(member_router, prefix="/member", tags=["Member"])
router.include_router(stat_router, prefix="/stat", tags=["Stat"])
