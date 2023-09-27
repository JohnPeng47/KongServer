from fastapi import APIRouter, Depends
from ..auth.utils import get_username_from_token


router = APIRouter()


@router.get("/events", )
def events(username: str = Depends(get_username_from_token)):
    return {"username": username}
