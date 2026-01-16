import pytest


def test_weighted_average_logic():
    """Testujemy samą funkcję matematyczną bez bazy danych."""
    from app.api.routes.reports import calculate_weighted_average
    from unittest.mock import MagicMock

    grade1 = MagicMock(value="5", weight=2.0)
    grade2 = MagicMock(value="4+", weight=1.0)

    avg = calculate_weighted_average([grade1, grade2])
    assert avg == 4.83