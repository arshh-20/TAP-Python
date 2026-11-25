import csv
import json


def read_csv(path: str) -> list[dict[str, str]]:
    """Read a CSV file into a list of dictionaries."""
    with open(path, newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def read_mapping(path: str) -> dict[str, str]:
    """Read a column mapping from a JSON file."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)
