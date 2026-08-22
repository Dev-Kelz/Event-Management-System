from fastapi import APIRouter

router = APIRouter()


@router.get("/notifications")
def list_notifications():
    return {"success": True, "notifications": []}
