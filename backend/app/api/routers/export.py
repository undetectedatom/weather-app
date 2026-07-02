from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.api.dependencies import CurrentUserDep, SessionDep
from app.services.export_service import ExportError, export_service

router = APIRouter()


@router.get("")
def export_history(format: str, session: SessionDep, user: CurrentUserDep) -> Response:
    try:
        export = export_service.export_records(session, user, format)
    except ExportError as exc:
        raise HTTPException(status_code=exc.status_code, detail={"code": exc.code, "message": str(exc), "details": None}) from exc

    return Response(
        content=export.content,
        media_type=export.media_type,
        headers={"Content-Disposition": f'attachment; filename="weather-history.{export.extension}"'},
    )
