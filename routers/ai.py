from fastapi import APIRouter
# ----------------------------------

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.get("/ping")
def aiml():
    return {
        "service":"ai",
        "status":"ok"
    }