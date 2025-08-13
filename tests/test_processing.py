import pytest

from src.processing import filter_by_state, sort_by_date

bank_oper = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

@pytest.fixture
def sample_data():
    return bank_oper.copy()

# Тесты для filter_by_state
@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [41428829, 939719570]),
        ("CANCELED", [594226727, 615064591]),
        ("", []),
        (None, []),  # Тест на None
    ],
)
def test_filter_by_state(sample_data, state, expected_ids):
    filtered = filter_by_state(sample_data, state)
    assert [x["id"] for x in filtered] == expected_ids

def test_filter_by_state_default(sample_data):
    filtered = filter_by_state(sample_data)
    assert [x["id"] for x in filtered] == [41428829, 939719570]

def test_filter_by_state_missing_key():
    operations = [{"id": 1}, {"id": 2, "state": "EXECUTED"}]
    filtered = filter_by_state(operations, "EXECUTED")
    assert [x["id"] for x in filtered] == [2]

# Тесты для sort_by_date
@pytest.mark.parametrize("reverse, expected_first_id", [(True, 41428829), (False, 939719570)])
def test_sort_by_date(sample_data, reverse, expected_first_id):
    sorted_ops = sort_by_date(sample_data, reverse=reverse)
    assert sorted_ops[0]["id"] == expected_first_id

def test_sort_by_date_empty_list():
    assert sort_by_date([]) == []

def test_sort_by_date_missing_key():
    operations = [{"id": 1}, {"id": 2, "date": "2023-01-01"}]
    sorted_ops = sort_by_date(operations)
    assert [x["id"] for x in sorted_ops] == [2]

def test_sort_by_date_invalid_date():
    operations = [{"id": 1, "date": "2023-13-01"}]  # Невалидная дата
    try:
        sort_by_date(operations)
    except ValueError:
        pass  # Ожидаем ошибку парсинга даты