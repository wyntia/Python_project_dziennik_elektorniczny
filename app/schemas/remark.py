from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class RemarkBase(BaseModel):
    """
    Podstawowy schemat uwagi zawierający punkty, opis i typ uwagi.
    Waliduje zakres punktów od -50 do 50.
    """
    points: int = Field(..., ge=-50, le=50, description="Ilość punktów w zakresie od -50 do 50")
    description: str = Field(..., min_length=1, description="Treść uwagi")
    is_positive: bool = Field(..., description="Określa, czy uwaga jest pozytywna (True) czy negatywna (False)")


class RemarkCreate(RemarkBase):
    """
    Schemat używany do tworzenia nowej uwagi. Wymaga ID ucznia i nauczyciela.
    """
    student_id: int
    teacher_id: int


class RemarkUpdate(BaseModel):
    """
    Schemat do edycji istniejącej uwagi. Wszystkie pola są opcjonalne.
    """
    points: Optional[int] = Field(None, ge=-50, le=50)
    description: Optional[str] = None
    is_positive: Optional[bool] = None


class Remark(RemarkBase):
    """
    Pełny schemat uwagi zwracany przez API, zawierający ID oraz datę wystawienia.
    """
    id: int
    student_id: int
    teacher_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)