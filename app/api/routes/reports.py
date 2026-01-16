from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal
import xml.etree.ElementTree as ET
from datetime import datetime

from app.db.session import get_db
from app.crud import crud_student
from app.models.Student import Student

router = APIRouter()

GRADE_MAP: dict[str, float] = {
    "6": 6.0, "5+": 5.5, "5": 5.0, "5-": 4.75,
    "4+": 4.5, "4": 4.0, "4-": 3.75,
    "3+": 3.5, "3": 3.0, "3-": 2.75,
    "2+": 2.5, "2": 2.0, "2-": 1.75, "1": 1.0
}


def calculate_weighted_average(grades: list) -> float:
    """
    Oblicza średnią ważoną na podstawie listy obiektów ocen.

    Args:
        grades (list): Lista obiektów Grade z bazy danych.

    Returns:
        float: Obliczona średnia zaokrąglona do 2 miejsc po przecinku.
    """
    if not grades:
        return 0.0

    total_points = sum(GRADE_MAP.get(g.value, 0.0) * g.weight for g in grades)
    total_weights = sum(g.weight for g in grades)

    return round(total_points / total_weights, 2) if total_weights > 0 else 0.0


def dict_to_xml(root_tag: str, d: dict) -> str:
    """
    Konwertuje słownik na format XML.
    """

    def build_xml(parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                sub = ET.SubElement(parent, key)
                build_xml(sub, value)
        elif isinstance(data, list):
            for item in data:
                sub = ET.SubElement(parent, "entry")
                build_xml(sub, item)
        else:
            parent.text = str(data)

    root = ET.Element(root_tag)
    build_xml(root, d)
    return ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')


@router.get("/student/{student_id}/download")
async def download_student_report(
        student_id: int,
        file_format: Literal["json", "xml"] = "json",
        db: AsyncSession = Depends(get_db)
) -> Response:
    """
    Generuje i wysyła raport o uczniu jako plik do pobrania.
    Zawiera średnią ważoną, listę ocen oraz szczegóły uwag.
    """
    student_data = await crud_student.get_student(db, student_id)
    if not student_data:
        raise HTTPException(status_code=404, detail="Student o podanym ID nie istnieje.")

    weighted_avg = calculate_weighted_average(student_data.grades)
    total_remark_points = sum(r.points for r in student_data.remarks)

    report_dict = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "student": {
            "full_name": f"{student_data.first_name} {student_data.last_name}",
            "pesel": student_data.pesel
        },
        "results": {
            "weighted_average": weighted_avg,
            "total_grades": len(student_data.grades)
        },
        "remarks_summary": {
            "total_points": total_remark_points,
            "list": [
                {
                    "points": r.points,
                    "text": r.description,
                    "date": r.created_at.strftime("%Y-%m-%d")
                } for r in student_data.remarks
            ]
        }
    }

    filename = f"report_student_{student_id}.{file_format}"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}

    if file_format == "xml":
        xml_content = dict_to_xml("StudentReport", report_dict)
        return Response(content=xml_content, media_type="application/xml", headers=headers)

    return JSONResponse(content=report_dict, headers=headers)