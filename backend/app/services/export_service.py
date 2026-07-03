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
        records = [self._serialize_record(record.model_dump(mode="json")) for record in history_service.list_records(session, user)]
        export_format = export_format.lower()
        if export_format == "json":
            return ExportPayload(json.dumps(records, indent=2, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8", "json")
        if export_format == "csv":
            return self._csv(records)
        if export_format == "xml":
            return self._xml(records)
        if export_format == "markdown":
            return self._markdown(records)
        raise ExportError("Unsupported export format")

    def _csv(self, records: list[dict]) -> ExportPayload:
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=[
                "id",
                "snapshot_type",
                "location_query",
                "resolved_name",
                "region",
                "country",
                "latitude",
                "longitude",
                "start_date",
                "end_date",
                "status",
                "notes",
                "source",
                "current_temperature_c",
                "current_feels_like_c",
                "current_condition",
                "current_humidity",
                "current_wind_speed",
                "range_average_temp_c",
                "range_max_temp_c",
                "range_min_temp_c",
                "forecast_days_count",
                "forecast_days_json",
                "created_at",
                "updated_at",
            ],
        )
        writer.writeheader()
        for record in records:
            writer.writerow({key: record.get(key) for key in writer.fieldnames})
        return ExportPayload(buffer.getvalue().encode("utf-8"), "text/csv; charset=utf-8", "csv")

    def _xml(self, records: list[dict]) -> ExportPayload:
        root = Element("weather_history")
        for record in records:
            item = SubElement(root, "record")
            for key in [
                "id",
                "snapshot_type",
                "location_query",
                "resolved_name",
                "region",
                "country",
                "latitude",
                "longitude",
                "start_date",
                "end_date",
                "status",
                "notes",
                "source",
                "current_temperature_c",
                "current_feels_like_c",
                "current_condition",
                "current_humidity",
                "current_wind_speed",
                "range_average_temp_c",
                "range_max_temp_c",
                "range_min_temp_c",
                "forecast_days_count",
                "created_at",
                "updated_at",
            ]:
                child = SubElement(item, key)
                child.text = "" if record.get(key) is None else str(record.get(key))
            forecast_days = SubElement(item, "forecast_days")
            for day in record.get("forecast_days", []):
                day_node = SubElement(forecast_days, "day")
                for key in ["date", "temp_max_c", "temp_min_c", "condition", "icon_code"]:
                    child = SubElement(day_node, key)
                    child.text = "" if day.get(key) is None else str(day.get(key))
        return ExportPayload(tostring(root, encoding="utf-8", xml_declaration=True), "application/xml; charset=utf-8", "xml")

    def _markdown(self, records: list[dict]) -> ExportPayload:
        lines = ["| ID | Query | Resolved | Dates | Status | Current | Range Summary | Forecast Days | Notes |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for record in records:
            date_label = record.get("start_date") or ""
            if record.get("start_date") and record.get("end_date") and record.get("start_date") != record.get("end_date"):
                date_label = f"{record.get('start_date')} to {record.get('end_date')}"
            elif record.get("end_date"):
                date_label = record.get("end_date")
            current_label = self._markdown_current_weather(record)
            range_label = self._markdown_range_summary(record)
            lines.append(
                f"| {record.get('id')} | {record.get('location_query')} | {record.get('resolved_name')} | {date_label} | {record.get('status')} | {current_label} | {range_label} | {record.get('forecast_days_count')} | {record.get('notes') or ''} |"
            )
            for day in record.get("forecast_days", []):
                lines.append(
                    f"|  |  |  |  |  |  |  | {day.get('date')}: {day.get('condition')} ({day.get('temp_min_c')} to {day.get('temp_max_c')} C) |  |"
                )
        return ExportPayload("\n".join(lines).encode("utf-8"), "text/markdown; charset=utf-8", "md")

    def _serialize_record(self, record: dict) -> dict:
        payload = record.get("weather_payload") or {}
        current = payload.get("current") or {}
        range_summary = payload.get("range_summary") or {}
        forecast_days = payload.get("forecast_days") or []
        return {
            "id": record.get("id"),
            "snapshot_type": record.get("snapshot_type"),
            "location_query": record.get("location_query"),
            "resolved_name": record.get("resolved_name"),
            "region": record.get("region"),
            "country": record.get("country"),
            "latitude": record.get("latitude"),
            "longitude": record.get("longitude"),
            "start_date": record.get("start_date"),
            "end_date": record.get("end_date"),
            "status": record.get("status"),
            "notes": record.get("notes"),
            "source": payload.get("source"),
            "current_temperature_c": current.get("temperature_c"),
            "current_feels_like_c": current.get("feels_like_c"),
            "current_condition": current.get("condition"),
            "current_humidity": current.get("humidity"),
            "current_wind_speed": current.get("wind_speed"),
            "range_average_temp_c": range_summary.get("average_temp_c"),
            "range_max_temp_c": range_summary.get("max_temp_c"),
            "range_min_temp_c": range_summary.get("min_temp_c"),
            "forecast_days_count": len(forecast_days),
            "forecast_days": forecast_days,
            "forecast_days_json": json.dumps(forecast_days, ensure_ascii=False),
            "weather_payload": payload,
            "created_at": record.get("created_at"),
            "updated_at": record.get("updated_at"),
        }

    def _markdown_current_weather(self, record: dict) -> str:
        if record.get("current_temperature_c") is None and not record.get("current_condition"):
            return ""
        parts = []
        if record.get("current_temperature_c") is not None:
            parts.append(f"{record['current_temperature_c']} C")
        if record.get("current_condition"):
            parts.append(str(record["current_condition"]))
        return " / ".join(parts)

    def _markdown_range_summary(self, record: dict) -> str:
        if record.get("range_average_temp_c") is None and record.get("range_max_temp_c") is None and record.get("range_min_temp_c") is None:
            return ""
        return (
            f"avg {record.get('range_average_temp_c')} C, "
            f"max {record.get('range_max_temp_c')} C, "
            f"min {record.get('range_min_temp_c')} C"
        )


export_service = ExportService()
