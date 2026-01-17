import pytest
from unittest.mock import MagicMock
from app.api.routes.reports import calculate_weighted_average, dict_to_xml


def test_calculate_weighted_average_success():
    """Testuje obliczanie średniej dla zestawu ocen o różnych wagach."""
    grade_5 = MagicMock(value="5", weight=2.0)
    grade_4_plus = MagicMock(value="4+", weight=1.0)
    grade_3_minus = MagicMock(value="3-", weight=1.0)

    grades = [grade_5, grade_4_plus, grade_3_minus]

    result = calculate_weighted_average(grades)
    assert result == 4.31


def test_calculate_weighted_average_empty():
    """Sprawdza zachowanie funkcji przy braku ocen."""
    assert calculate_weighted_average([]) == 0.0


def test_dict_to_xml_conversion():
    """Weryfikuje, czy słownik jest poprawnie zamieniany na ciąg znaków XML."""
    data = {"student": "Jan", "points": 10}
    xml_output = dict_to_xml("Report", data)

    assert "<Report>" in xml_output
    assert "<student>Jan</student>" in xml_output
    assert "<points>10</points>" in xml_output