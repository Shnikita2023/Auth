from fastapi import APIRouter
from .user.routers import router as router_user

router = APIRouter()
router.include_router(router=router_user)
