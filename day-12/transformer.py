import re
from datetime import datetime


def to_snake_case(column: str) -> str:
    """Convert a column name to snake_case."""
    column = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", column)
    return re.sub(r"[^a-zA-Z0-9]+", "_", column).strip("_").lower()


def normalize_columns(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Convert row keys to snake_case."""
    return [
        {to_snake_case(column): value for column, value in row.items()}
        for row in rows
    ]


def map_columns(
    rows: list[dict[str, str]], mapping: dict[str, str]
) -> list[dict[str, str]]:
    """Rename row keys using a column mapping."""
    return [
        {mapping.get(column, column): value for column, value in row.items()}
        for row in rows
    ]


def convert_values(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Convert price, freight, and date values to their proper types."""
    converted_rows = []
    for row in rows:
        converted_row = {}
        for column, value in row.items():
            if value == "":
                converted_value = None
            elif column in ("price", "freight", "freight_value"):
                converted_value = float(value)
            elif column.endswith(("_date", "_timestamp", "_at")):
                converted_value = datetime.fromisoformat(value)
            else:
                converted_value = value
            converted_row[column] = converted_value
        converted_rows.append(converted_row)
    return converted_rows


def transform_rows(
    rows: list[dict[str, str]], mapping: dict[str, str]
) -> list[dict[str, object]]:
    """Rename columns and convert numeric and timestamp values."""
    rows = normalize_columns(rows)
    rows = map_columns(rows, mapping)
    return convert_values(rows)


def calculate_order_totals(rows: list[dict[str, object]]) -> dict[str, float]:
    """Calculate item price and freight totals for each order."""
    totals = {}
    for row in rows:
        order_id = row["order_id"]
        if not isinstance(order_id, str):
            raise TypeError("order_id must be a string")
        total = totals.get(order_id, 0.0) + float(row["price"]) + float(row["freight"])
        totals[order_id] = round(total, 2)
    return totals
