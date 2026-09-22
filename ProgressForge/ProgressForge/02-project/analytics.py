"""Progress calculations for ProgressForge.

The functions here use simple, transparent calculations so the user can
understand and explain how each result is produced.
"""

from datetime import date, datetime, timedelta
from statistics import mean


def to_float(value, default=0.0) -> float:
    """Convert a value to float without crashing on bad stored data."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def to_int(value, default=0) -> int:
    """Convert a value to int without crashing on bad stored data."""
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def parse_date(value: str):
    """Convert an ISO YYYY-MM-DD string into a date, or return None."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def calculate_volume(sets: int, reps: int, weight: float) -> float:
    """Calculate simple training volume: sets × reps × weight."""
    return round(sets * reps * weight, 2)


def percentage_change(old_value: float, new_value: float):
    """Return percentage change, or None when the old value is zero."""
    if old_value == 0:
        return None
    return round(((new_value - old_value) / old_value) * 100, 1)


def sort_records_by_date(records: list[dict]) -> list[dict]:
    """Return valid dated records in oldest-to-newest order."""
    valid_records = []
    for record in records:
        record_date = parse_date(record.get("date", ""))
        if record_date is not None:
            copied = dict(record)
            copied["_parsed_date"] = record_date
            valid_records.append(copied)

    def date_key(item):
        return item["_parsed_date"]

    valid_records.sort(key=date_key)
    return valid_records


def get_exercise_records(workouts: list[dict], exercise_name: str) -> list[dict]:
    """Return all workout records for one exercise in date order."""
    matching = []
    for record in workouts:
        if record.get("exercise") == exercise_name:
            matching.append(record)
    return sort_records_by_date(matching)


def get_previous_performance(workouts: list[dict], exercise_name: str):
    """Return the most recent performance for an exercise, if one exists."""
    records = get_exercise_records(workouts, exercise_name)
    if not records:
        return None
    return records[-1]


def get_personal_best(workouts: list[dict], exercise_name: str):
    """Return the record with the highest logged weight for an exercise."""
    records = get_exercise_records(workouts, exercise_name)
    if not records:
        return None

    best = records[0]
    for record in records[1:]:
        if to_float(record.get("weight")) > to_float(best.get("weight")):
            best = record
    return best


def is_new_personal_record(workouts: list[dict], exercise_name: str, new_weight: float):
    """Check whether a new weight is above the previous highest weight."""
    previous_best = get_personal_best(workouts, exercise_name)
    if previous_best is None:
        return False, None

    old_best_weight = to_float(previous_best.get("weight"))
    return new_weight > old_best_weight, old_best_weight


def compare_performances(previous: dict | None, current: dict) -> dict:
    """Compare one current workout record with the previous record."""
    current_weight = to_float(current.get("weight"))
    current_volume = to_float(current.get("volume"))

    if previous is None:
        return {
            "has_previous": False,
            "current_weight": current_weight,
            "current_volume": current_volume,
        }

    previous_weight = to_float(previous.get("weight"))
    previous_volume = to_float(previous.get("volume"))
    weight_change = current_weight - previous_weight
    volume_change = current_volume - previous_volume

    if current_volume > previous_volume:
        result = "Improvement from previous session"
    elif current_volume < previous_volume:
        result = "Lower recorded training volume than previous session"
    else:
        result = "Same recorded training volume as previous session"

    return {
        "has_previous": True,
        "previous_weight": previous_weight,
        "current_weight": current_weight,
        "weight_change": round(weight_change, 2),
        "weight_change_percent": percentage_change(previous_weight, current_weight),
        "previous_volume": previous_volume,
        "current_volume": current_volume,
        "volume_change": round(volume_change, 2),
        "volume_change_percent": percentage_change(previous_volume, current_volume),
        "result": result,
    }


def analyse_exercise_progress(workouts: list[dict], exercise_name: str):
    """Create a simple progress summary for one exercise."""
    records = get_exercise_records(workouts, exercise_name)
    if not records:
        return None

    first = records[0]
    latest = records[-1]
    best = get_personal_best(workouts, exercise_name)

    first_weight = to_float(first.get("weight"))
    latest_weight = to_float(latest.get("weight"))
    first_volume = to_float(first.get("volume"))
    latest_volume = to_float(latest.get("volume"))

    return {
        "records": records,
        "first_weight": first_weight,
        "latest_weight": latest_weight,
        "highest_weight": to_float(best.get("weight")) if best else latest_weight,
        "first_volume": first_volume,
        "latest_volume": latest_volume,
        "weight_change": round(latest_weight - first_weight, 2),
        "weight_change_percent": percentage_change(first_weight, latest_weight),
        "volume_change": round(latest_volume - first_volume, 2),
        "volume_change_percent": percentage_change(first_volume, latest_volume),
        "sessions_recorded": len(records),
    }


def progress_leaderboard(workouts: list[dict]) -> list[dict]:
    """Rank exercises by first-to-latest recorded weight percentage change."""
    exercise_names = []
    for record in workouts:
        name = record.get("exercise")
        if name and name not in exercise_names:
            exercise_names.append(name)

    results = []
    for name in exercise_names:
        analysis = analyse_exercise_progress(workouts, name)
        if analysis and analysis["sessions_recorded"] >= 2:
            change = analysis["weight_change_percent"]
            if change is not None:
                results.append({"exercise": name, "change_percent": change})

    results.sort(key=lambda item: item["change_percent"], reverse=True)
    return results


def progress_watch_status(workouts: list[dict], exercise_name: str) -> dict:
    """Analyse the last three training volumes using simple transparent rules.

    Rules:
    - fewer than 3 records -> NOT ENOUGH DATA
    - latest volume > first recent volume by more than 2% -> IMPROVING
    - latest volume < first recent volume by more than 2% -> RECENT DECREASE
    - all three volumes are equal -> NO RECENT CHANGE
    - otherwise -> STABLE
    """
    records = get_exercise_records(workouts, exercise_name)
    if len(records) < 3:
        return {"status": "NOT ENOUGH DATA", "recent_records": records}

    recent = records[-3:]
    volumes = [to_float(record.get("volume")) for record in recent]
    first_volume = volumes[0]
    latest_volume = volumes[-1]
    change = percentage_change(first_volume, latest_volume)

    if volumes[0] == volumes[1] == volumes[2]:
        status = "NO RECENT CHANGE"
    elif change is not None and change > 2:
        status = "IMPROVING"
    elif change is not None and change < -2:
        status = "RECENT DECREASE"
    else:
        status = "STABLE"

    return {
        "status": status,
        "recent_records": recent,
        "change_percent": change,
    }


def personal_records(workouts: list[dict]) -> list[dict]:
    """Return the highest recorded weight for every exercise."""
    names = []
    for record in workouts:
        name = record.get("exercise")
        if name and name not in names:
            names.append(name)

    records = []
    for name in names:
        best = get_personal_best(workouts, name)
        if best:
            records.append(
                {
                    "exercise": name,
                    "weight": to_float(best.get("weight")),
                    "date": best.get("date", ""),
                    "reps": to_int(best.get("reps")),
                    "sets": to_int(best.get("sets")),
                }
            )
    records.sort(key=lambda item: item["exercise"].lower())
    return records


def analyse_bodyweight(records: list[dict]):
    """Summarise body-weight history using rolling seven-day date windows."""
    sorted_records = sort_records_by_date(records)
    if not sorted_records:
        return None

    weights = [to_float(record.get("weight")) for record in sorted_records]
    first_weight = weights[0]
    latest_weight = weights[-1]
    latest_date = sorted_records[-1]["_parsed_date"]

    current_start = latest_date - timedelta(days=6)
    previous_end = current_start - timedelta(days=1)
    previous_start = previous_end - timedelta(days=6)

    current_records = records_between(sorted_records, current_start, latest_date)
    previous_records = records_between(sorted_records, previous_start, previous_end)

    current_weights = [to_float(record.get("weight")) for record in current_records]
    previous_weights = [to_float(record.get("weight")) for record in previous_records]

    return {
        "first_weight": first_weight,
        "latest_weight": latest_weight,
        "total_change": round(latest_weight - first_weight, 2),
        "total_change_percent": percentage_change(first_weight, latest_weight),
        "current_7_average": round(mean(current_weights), 2) if current_weights else None,
        "previous_7_average": round(mean(previous_weights), 2) if previous_weights else None,
        "entries": len(sorted_records),
    }


def analyse_nutrition(records: list[dict], protein_target: float, calorie_target: float):
    """Summarise calories and protein from all provided nutrition records."""
    sorted_records = sort_records_by_date(records)
    if not sorted_records:
        return None

    calories = [to_float(record.get("calories")) for record in sorted_records]
    proteins = [to_float(record.get("protein")) for record in sorted_records]

    days_protein_target = 0
    for protein in proteins:
        if protein >= protein_target:
            days_protein_target += 1

    return {
        "average_calories": round(mean(calories), 1),
        "average_protein": round(mean(proteins), 1),
        "protein_target": protein_target,
        "calorie_target": calorie_target,
        "days_protein_target": days_protein_target,
        "entries": len(sorted_records),
        "protein_difference": round(mean(proteins) - protein_target, 1),
    }


def records_between(records: list[dict], start_date: date, end_date: date) -> list[dict]:
    """Return records whose ISO date falls inside an inclusive period."""
    matches = []
    for record in records:
        record_date = parse_date(record.get("date", ""))
        if record_date and start_date <= record_date <= end_date:
            matches.append(record)
    return sort_records_by_date(matches)


def unique_session_count(workouts: list[dict]) -> int:
    """Count workout sessions using unique date + routine combinations."""
    sessions = set()
    for record in workouts:
        record_date = record.get("date", "")
        routine = record.get("routine", "") or "Quick Log"
        if record_date:
            sessions.add((record_date, routine))
    return len(sessions)


def count_personal_records_in_period(workouts: list[dict], start_date: date, end_date: date) -> int:
    """Count new highest-weight records achieved during a date period."""
    sorted_records = sort_records_by_date(workouts)
    best_weights = {}
    count = 0

    for record in sorted_records:
        exercise = record.get("exercise", "")
        record_date = record.get("_parsed_date")
        weight = to_float(record.get("weight"))

        previous_best = best_weights.get(exercise)
        if previous_best is not None and weight > previous_best:
            if start_date <= record_date <= end_date:
                count += 1

        if previous_best is None or weight > previous_best:
            best_weights[exercise] = weight

    return count


def weekly_report(
    workouts: list[dict],
    bodyweights: list[dict],
    nutrition: list[dict],
    settings: dict,
    report_end: date | None = None,
) -> dict:
    """Build a rolling seven-day report plus comparison with the prior seven days."""
    if report_end is None:
        report_end = date.today()

    current_start = report_end - timedelta(days=6)
    previous_end = current_start - timedelta(days=1)
    previous_start = previous_end - timedelta(days=6)

    current_workouts = records_between(workouts, current_start, report_end)
    previous_workouts = records_between(workouts, previous_start, previous_end)
    current_bodyweights = records_between(bodyweights, current_start, report_end)
    previous_bodyweights = records_between(bodyweights, previous_start, previous_end)
    current_nutrition = records_between(nutrition, current_start, report_end)

    current_volume = round(sum(to_float(record.get("volume")) for record in current_workouts), 2)
    previous_volume = round(sum(to_float(record.get("volume")) for record in previous_workouts), 2)

    workout_target = int(settings.get("weekly_workout_target", 5))
    current_sessions = unique_session_count(current_workouts)
    completion_percent = round((current_sessions / workout_target) * 100, 1) if workout_target else None

    # Compare latest current-week weight with the latest earlier record for each exercise.
    exercises_improved = 0
    exercises_stable = 0
    best_progress = None

    exercise_names = []
    for record in current_workouts:
        name = record.get("exercise")
        if name and name not in exercise_names:
            exercise_names.append(name)

    all_sorted = sort_records_by_date(workouts)
    for name in exercise_names:
        current_records_for_exercise = get_exercise_records(current_workouts, name)
        if not current_records_for_exercise:
            continue
        latest_current = current_records_for_exercise[-1]
        current_weight = to_float(latest_current.get("weight"))

        earlier_records = []
        for record in all_sorted:
            if record.get("exercise") == name and record.get("_parsed_date") < current_start:
                earlier_records.append(record)

        if not earlier_records:
            continue

        previous_record = earlier_records[-1]
        previous_weight = to_float(previous_record.get("weight"))
        change_percent = percentage_change(previous_weight, current_weight)

        if change_percent is None:
            continue
        if change_percent > 0:
            exercises_improved += 1
            if best_progress is None or change_percent > best_progress["change_percent"]:
                best_progress = {
                    "exercise": name,
                    "previous_weight": previous_weight,
                    "current_weight": current_weight,
                    "change_percent": change_percent,
                }
        else:
            exercises_stable += 1

    current_bw_average = None
    previous_bw_average = None
    if current_bodyweights:
        current_bw_average = round(mean(to_float(item.get("weight")) for item in current_bodyweights), 2)
    if previous_bodyweights:
        previous_bw_average = round(mean(to_float(item.get("weight")) for item in previous_bodyweights), 2)

    protein_target = float(settings.get("daily_protein_target", 130))
    average_protein = None
    protein_target_days = 0
    if current_nutrition:
        protein_values = [to_float(item.get("protein")) for item in current_nutrition]
        average_protein = round(mean(protein_values), 1)
        protein_target_days = sum(1 for value in protein_values if value >= protein_target)

    summary = []
    if current_sessions == 0:
        summary.append("No workouts were recorded in this seven-day period.")
    elif completion_percent is not None and completion_percent >= 100:
        summary.append("Your recorded workout target was reached this period.")
    else:
        summary.append("Your recorded workout target was not fully reached this period.")

    volume_change_percent = percentage_change(previous_volume, current_volume)
    if previous_volume > 0 and volume_change_percent is not None:
        if volume_change_percent > 2:
            summary.append("Recorded training volume increased compared with the previous seven days.")
        elif volume_change_percent < -2:
            summary.append("Recorded training volume decreased compared with the previous seven days.")
        else:
            summary.append("Recorded training volume was similar to the previous seven days.")

    if average_protein is not None:
        if average_protein >= protein_target:
            summary.append("Average recorded protein met or exceeded your personal target.")
        else:
            summary.append("Average recorded protein was below your personal target.")

    return {
        "current_start": current_start,
        "current_end": report_end,
        "previous_start": previous_start,
        "previous_end": previous_end,
        "current_sessions": current_sessions,
        "weekly_target": workout_target,
        "completion_percent": completion_percent,
        "exercises_improved": exercises_improved,
        "exercises_stable": exercises_stable,
        "personal_records": count_personal_records_in_period(workouts, current_start, report_end),
        "best_progress": best_progress,
        "current_volume": current_volume,
        "previous_volume": previous_volume,
        "volume_change_percent": volume_change_percent,
        "current_bw_average": current_bw_average,
        "previous_bw_average": previous_bw_average,
        "bodyweight_change": round(current_bw_average - previous_bw_average, 2)
        if current_bw_average is not None and previous_bw_average is not None
        else None,
        "protein_target": protein_target,
        "average_protein": average_protein,
        "protein_target_days": protein_target_days,
        "nutrition_days": len(current_nutrition),
        "summary": summary,
    }
