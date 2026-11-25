def validate_rows(rows: list[dict[str, str]], required_columns: list[str]) -> None:
    """Check that rows contain the required columns."""
    if not rows:
        raise ValueError("CSV has no data rows")

    missing = [column for column in required_columns if column not in rows[0]]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
