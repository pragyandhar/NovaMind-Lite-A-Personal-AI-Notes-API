from fastapi import APIRouter
# ------------------------------

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/ping")
def authentication():
    return {
        "service":"auth",
        "status":"ok"
    }