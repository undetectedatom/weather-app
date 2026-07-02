from __future__ import annotations

import csv
import io
import json
from xml.etree.ElementTree import Element, SubElement, tostring

from sqlmodel import Session

from app.database.models import User
from app.services.history_service import history_service


class ExportError(Exception):
    def __init__(self, message: str, code: str = "INVALID_EXPORT_FORMAT", status_code: int = 400):
        super().__init__(message)
        self.code = code
        self.status_code = status_code


class ExportPayload:
    def __init__(self, content: bytes, media_type: str, extension: str) -> None:
        self.content = content
        self.media_type = media_type
        self.extension = extension


class ExportService:
    def export_records(self, session: Session, user: User, export_format: str) -> ExportPayload:
        records = [record.model_dump(mode="json") for record in history_service.list_records(session, user)]
        export_format = export_format.lower()
        if export_format == "json":
            return ExportPayload(json.dumps(records, indent=2).encode(), "application/json", "json")
        if export_format == "csv":
            return self._csv(records)
        if export_format == "xml":
            return self._xml(records)
        if export_format == "markdown":
            return self._markdown(records)
        raise ExportError("Unsupported export format")

    def _csv(self, records: list[dict]) -> ExportPayload:
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=["id", "location_query", "resolved_name", "start_date", "end_date", "status", "created_at"])
        writer.writeheader()
        for record in records:
            writer.writerow({key: record.get(key) for key in writer.fieldnames})
        return ExportPayload(buffer.getvalue().encode(), "text/csv", "csv")

    def _xml(self, records: list[dict]) -> ExportPayload:
        root = Element("weather_history")
        for record in records:
            item = SubElement(root, "record")
            for key in ["id", "location_query", "resolved_name", "start_date", "end_date", "status", "created_at"]:
                child = SubElement(item, key)
                child.text = "" if record.get(key) is None else str(record.get(key))
        return ExportPayload(tostring(root), "application/xml", "xml")

    def _markdown(self, records: list[dict]) -> ExportPayload:
        lines = ["| ID | Query | Resolved | Start | End | Status |", "| --- | --- | --- | --- | --- | --- |"]
        for record in records:
            lines.append(f"| {record.get('id')} | {record.get('location_query')} | {record.get('resolved_name')} | {record.get('start_date') or ''} | {record.get('end_date') or ''} | {record.get('status')} |")
        return ExportPayload("\n".join(lines).encode(), "text/markdown", "md")


export_service = ExportService()
