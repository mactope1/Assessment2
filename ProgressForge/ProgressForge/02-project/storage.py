"""File storage helpers for ProgressForge.

This module keeps reading/writing logic separate from the command-line interface.
"""

import csv
import json
from copy import deepcopy
from pathlib import Path

from config import (
    BODYWEIGHT_FIELDS,
    BODYWEIGHT_FILE,
    DATA_DIR,
    DEFAULT_EXERCISES,
    DEFAULT_ROUTINES,
    DEFAULT_SETTINGS,
    EXERCISES_FILE,
    NUTRITION_FIELDS,
    NUTRITION_FILE,
    ROUTINES_FILE,
    SETTINGS_FILE,
    WORKOUT_FIELDS,
    WORKOUTS_FILE,
)


def ensure_csv_file(path: Path, fieldnames: list[str]) -> None:
    """Create a CSV file with headers if it does not already exist."""
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()


def save_json(path: Path, data) -> None:
    """Save Python data as readable JSON."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_json(path: Path, default):
    """Load JSON, returning a safe default if the file is missing or invalid."""
    if not path.exists():
        return deepcopy(default)

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return deepcopy(default)


def ensure_data_files() -> None:
    """Create the ProgressForge data folder and starter files when needed."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not EXERCISES_FILE.exists():
        save_json(EXERCISES_FILE, DEFAULT_EXERCISES)

    if not ROUTINES_FILE.exists():
        save_json(ROUTINES_FILE, DEFAULT_ROUTINES)

    if not SETTINGS_FILE.exists():
        save_json(SETTINGS_FILE, DEFAULT_SETTINGS)

    ensure_csv_file(WORKOUTS_FILE, WORKOUT_FIELDS)
    ensure_csv_file(BODYWEIGHT_FILE, BODYWEIGHT_FIELDS)
    ensure_csv_file(NUTRITION_FILE, NUTRITION_FIELDS)


def load_csv(path: Path) -> list[dict]:
    """Read a CSV file into a list of dictionaries."""
    if not path.exists():
        return []

    try:
        with path.open("r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except OSError:
        return []


def append_csv(path: Path, fieldnames: list[str], row: dict) -> None:
    """Append one row to a CSV file."""
    file_exists = path.exists()

    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists or path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(row)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    """Rewrite a CSV file using the supplied rows."""
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def get_exercises() -> list[dict]:
    return load_json(EXERCISES_FILE, DEFAULT_EXERCISES)


def save_exercises(exercises: list[dict]) -> None:
    save_json(EXERCISES_FILE, exercises)


def get_routines() -> dict[str, list[str]]:
    return load_json(ROUTINES_FILE, DEFAULT_ROUTINES)


def save_routines(routines: dict[str, list[str]]) -> None:
    save_json(ROUTINES_FILE, routines)


def get_settings() -> dict:
    settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)
    for key, value in DEFAULT_SETTINGS.items():
        settings.setdefault(key, value)
    return settings


def save_settings(settings: dict) -> None:
    save_json(SETTINGS_FILE, settings)


def get_workouts() -> list[dict]:
    return load_csv(WORKOUTS_FILE)


def add_workout(record: dict) -> None:
    append_csv(WORKOUTS_FILE, WORKOUT_FIELDS, record)


def get_bodyweights() -> list[dict]:
    return load_csv(BODYWEIGHT_FILE)


def add_bodyweight(record: dict) -> None:
    """Save one body-weight value per date, replacing the same date if needed."""
    records = get_bodyweights()
    updated = False
    for index, existing in enumerate(records):
        if existing.get("date") == record.get("date"):
            records[index] = record
            updated = True
            break

    if not updated:
        records.append(record)
    write_csv(BODYWEIGHT_FILE, BODYWEIGHT_FIELDS, records)


def get_nutrition() -> list[dict]:
    return load_csv(NUTRITION_FILE)


def add_nutrition(record: dict) -> None:
    """Save one nutrition summary per date, replacing the same date if needed."""
    records = get_nutrition()
    updated = False
    for index, existing in enumerate(records):
        if existing.get("date") == record.get("date"):
            records[index] = record
            updated = True
            break

    if not updated:
        records.append(record)
    write_csv(NUTRITION_FILE, NUTRITION_FIELDS, records)
