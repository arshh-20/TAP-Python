import json
from collections.abc import Iterable
from pathlib import Path

import pandas as pd


class MissingRequiredColumnError(Exception):
    pass


def get_unprocessed_files(files: list[Path], processed_files: list[str]) -> list[Path]:
    return [file for file in files if file.name not in processed_files]


def apply_column_mapping(dataframe: pd.DataFrame, column_mapping: dict[str, str]) -> pd.DataFrame:
    return dataframe.rename(columns=column_mapping)


def get_required_columns(
    name: str, configured_required_columns: dict[str, list[str]]
) -> list[str]:
    if name not in configured_required_columns:
        raise MissingRequiredColumnError(f"{name} has no required columns configured")
    return configured_required_columns[name]


def check_required_columns(
    name: str, columns: Iterable[str], required_columns: Iterable[str]
) -> None:
    missing_columns = [column for column in required_columns if column not in columns]
    if missing_columns:
        raise MissingRequiredColumnError(
            f"{name} is missing required columns: {', '.join(missing_columns)}"
        )


def find_missing_fields(row: dict[str, object], required_columns: list[str]) -> list[str]:
    return [column for column in required_columns if pd.isna(row[column])]


def make_bad_record(
    source_file: str,
    row_number: int,
    row: dict[str, object],
    missing_fields: list[str],
) -> dict[str, object]:
    bad_record = dict(row)
    bad_record["source_file"] = source_file
    bad_record["row_number"] = row_number
    bad_record["reason"] = f"Missing required fields: {', '.join(missing_fields)}"
    return bad_record


def save_manifest(
    manifest_file: Path, processed_files: list[str], new_files: list[str]
) -> list[str]:
    updated_files = processed_files.copy()
    for file_name in new_files:
        if file_name not in updated_files:
            updated_files.append(file_name)

    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    with manifest_file.open("w", encoding="utf-8") as file:
        json.dump(updated_files, file, indent=2)

    return updated_files
