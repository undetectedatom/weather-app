from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import CurrentUserDep, SessionDep
from app.schemas.history import HistoryCreate, HistoryListResponse, HistoryPublic, HistoryUpdate
from app.services.history_service import HistoryError, history_service

router = APIRouter()


@router.post("", response_model=HistoryPublic, status_code=status.HTTP_201_CREATED)
async def create_history(payload: HistoryCreate, session: SessionDep, user: CurrentUserDep) -> HistoryPublic:
    try:
        return await history_service.create_record(session, user, payload)
    except HistoryError as exc:
        raise HTTPException(status_code=exc.status_code, detail={"code": exc.code, "message": str(exc), "details": None}) from exc


@router.get("", response_model=HistoryListResponse)
def list_history(session: SessionDep, user: CurrentUserDep) -> HistoryListResponse:
    return HistoryListResponse(records=history_service.list_records(session, user))


@router.get("/{record_id}", response_model=HistoryPublic)
def get_history(record_id: str, session: SessionDep, user: CurrentUserDep) -> HistoryPublic:
    try:
        return history_service.get_record(session, user, record_id)
    except HistoryError as exc:
        raise HTTPException(status_code=exc.status_code, detail={"code": exc.code, "message": str(exc), "details": None}) from exc


@router.patch("/{record_id}", response_model=HistoryPublic)
async def update_history(record_id: str, payload: HistoryUpdate, session: SessionDep, user: CurrentUserDep) -> HistoryPublic:
    try:
        return await history_service.update_record(session, user, record_id, payload)
    except HistoryError as exc:
        raise HTTPException(status_code=exc.status_code, detail={"code": exc.code, "message": str(exc), "details": None}) from exc


@router.delete("/{record_id}", response_model=dict[str, str])
def delete_history(record_id: str, session: SessionDep, user: CurrentUserDep) -> dict[str, str]:
    try:
        history_service.delete_record(session, user, record_id)
    except HistoryError as exc:
        raise HTTPException(status_code=exc.status_code, detail={"code": exc.code, "message": str(exc), "details": None}) from exc
    return {"message": "Record deleted"}
