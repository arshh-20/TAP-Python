from datetime import datetime
from pathlib import Path

from reader import read_csv, read_mapping
from transformer import calculate_order_totals, transform_rows


def test_read_csv_returns_dictionaries(tmp_path: Path) -> None:
    path = tmp_path / "sample.csv"
    path.write_text("order_id,price\n1,12.5\n", encoding="utf-8")

    assert read_csv(str(path)) == [{"order_id": "1", "price": "12.5"}]


def test_transform_rows_normalizes_and_converts() -> None:
    rows = [{
        "Order ID": "order-1",
        "Price": "10.5",
        "Freight Value": "2.5",
        "Order Purchase Timestamp": "2018-01-01 10:30:00",
    }]
    mapping = read_mapping("column_mapping.json")

    result = transform_rows(rows, mapping)[0]

    assert result["price"] == 10.5
    assert result["freight"] == 2.5
    assert result["purchased_at"] == datetime(2018, 1, 1, 10, 30)


def test_calculate_order_totals_groups_items() -> None:
    rows = [
        {"order_id": "one", "price": 10.0, "freight": 2.0},
        {"order_id": "one", "price": 5.0, "freight": 1.0},
        {"order_id": "two", "price": 7.0, "freight": 3.0},
    ]

    assert calculate_order_totals(rows) == {"one": 18.0, "two": 10.0}
