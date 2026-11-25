import json
from pathlib import Path

import pandas as pd
import pytest
import yaml
from pipeline_helpers import (
    MissingRequiredColumnError,
    apply_column_mapping,
    check_required_columns,
    find_missing_fields,
    get_required_columns,
    get_unprocessed_files,
    make_bad_record,
    save_manifest,
)


def test_get_unprocessed_files_skips_processed_files(tmp_path: Path) -> None:
    files = [tmp_path / "first.csv", tmp_path / "second.csv"]

    assert get_unprocessed_files(files, ["first.csv"]) == [files[1]]


def test_check_required_columns_accepts_complete_columns() -> None:
    check_required_columns("orders", ["order_id", "status"], ["order_id", "status"])


def test_check_required_columns_raises_for_missing_column() -> None:
    with pytest.raises(MissingRequiredColumnError, match="missing required columns: status"):
        check_required_columns("orders", ["order_id"], ["order_id", "status"])


def test_get_required_columns_raises_when_dataset_is_not_configured() -> None:
    with pytest.raises(MissingRequiredColumnError, match="has no required columns configured"):
        get_required_columns("new_dataset", {})


def test_find_missing_fields_returns_empty_fields() -> None:
    row = {"order_id": "order-1", "status": None, "price": float("nan")}

    assert find_missing_fields(row, ["order_id", "status", "price"]) == ["status", "price"]


def test_make_bad_record_adds_source_row_and_reason() -> None:
    row = {"order_id": "order-1", "status": None}

    result = make_bad_record("orders.csv", 4, row, ["status"])

    assert result["source_file"] == "orders.csv"
    assert result["row_number"] == 4
    assert result["reason"] == "Missing required fields: status"
    assert result["order_id"] == "order-1"


def test_save_manifest_adds_new_files_without_duplicates(tmp_path: Path) -> None:
    manifest_file = tmp_path / "manifest.json"

    result = save_manifest(manifest_file, ["first.csv"], ["second.csv", "first.csv"])

    assert result == ["first.csv", "second.csv"]
    assert json.loads(manifest_file.read_text(encoding="utf-8")) == result


def test_new_csv_extra_column_can_be_mapped_from_yaml_config(tmp_path: Path) -> None:
    csv_file = tmp_path / "reviewer_feedback.csv"
    csv_file.write_text(
        "order_id,order_status,reviewer_note\norder-1,delivered,fast\n",
        encoding="utf-8",
    )
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        "column_mapping:\n"
        "  order_status: status\n"
        "  reviewer_note: review_comment\n"
        "required_columns:\n"
        "  reviewer_feedback:\n"
        "    - order_id\n"
        "    - status\n"
        "    - review_comment\n",
        encoding="utf-8",
    )

    config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
    dataframe = pd.read_csv(csv_file)
    mapped_dataframe = apply_column_mapping(dataframe, config["column_mapping"])
    required_columns = get_required_columns(
        "reviewer_feedback", config["required_columns"]
    )
    check_required_columns(
        "reviewer_feedback", mapped_dataframe.columns, required_columns
    )

    assert mapped_dataframe.loc[0, "review_comment"] == "fast"
