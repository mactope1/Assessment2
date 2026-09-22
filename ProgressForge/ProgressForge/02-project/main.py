"""ProgressForge command-line application.

ProgressForge is a personal training memory and progress engine built for
ISYS5002 Introduction to Programming Assessment 2.
"""

from datetime import date, datetime

from analytics import (
    analyse_bodyweight,
    analyse_exercise_progress,
    analyse_nutrition,
    calculate_volume,
    compare_performances,
    get_personal_best,
    get_previous_performance,
    is_new_personal_record,
    personal_records,
    progress_leaderboard,
    progress_watch_status,
    to_float,
    to_int,
    weekly_report,
)
from config import APP_NAME, APP_TAGLINE
from storage import (
    add_bodyweight,
    add_nutrition,
    add_workout,
    ensure_data_files,
    get_bodyweights,
    get_exercises,
    get_nutrition,
    get_routines,
    get_settings,
    get_workouts,
    save_exercises,
    save_routines,
    save_settings,
)

WIDTH = 58


def line(character="-"):
    print(character * WIDTH)


def heading(title: str):
    print()
    line("=")
    print(title.center(WIDTH))
    line("=")


def pause():
    input("\nPress Enter to return to the menu...")


def format_date(date_text: str) -> str:
    try:
        return datetime.strptime(date_text, "%Y-%m-%d").strftime("%d %b %Y")
    except ValueError:
        return date_text


def get_positive_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if number > 0:
                return number
        except ValueError:
            number = None
        print("Invalid input. Please enter a whole number greater than 0.")


def get_positive_float(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
            if number > 0:
                return number
        except ValueError:
            number = None
        print("Invalid input. Please enter a number greater than 0.")


def get_optional_positive_float(prompt: str, current: float) -> float:
    while True:
        value = input(prompt).strip()
        if value == "":
            return current
        try:
            number = float(value)
            if number > 0:
                return number
        except ValueError:
            number = None
        print("Invalid input. Please enter a number greater than 0, or press Enter to keep the current value.")


def get_optional_positive_int(prompt: str, current: int) -> int:
    while True:
        value = input(prompt).strip()
        if value == "":
            return current
        try:
            number = int(value)
            if number > 0:
                return number
        except ValueError:
            number = None
        print("Invalid input. Please enter a whole number greater than 0, or press Enter to keep the current value.")


def choose_from_list(items: list, title: str, label_function=None):
    if not items:
        print("No options are currently available.")
        return None

    print(f"\n{title}")
    line()
    for index, item in enumerate(items, start=1):
        label = label_function(item) if label_function else str(item)
        print(f"{index}. {label}")
    print("0. Cancel")

    while True:
        choice = input("Choose an option: ").strip()
        if choice == "0":
            return None
        try:
            number = int(choice)
            if 1 <= number <= len(items):
                return items[number - 1]
        except ValueError:
            number = None
        print("Invalid choice. Please select a number shown above.")


def display_main_menu():
    print()
    line("=")
    print(APP_NAME.upper().center(WIDTH))
    print(APP_TAGLINE.upper().center(WIDTH))
    line("=")
    print("\nTODAY")
    print("1.  Start Today's Workout")
    print("2.  Quick Log Exercise")
    print("3.  Record Body Weight")
    print("4.  Record Nutrition")
    print("\nMY TRAINING")
    print("5.  My Exercise Vault")
    print("6.  My Routines")
    print("7.  Workout History")
    print("8.  Training Memory")
    print("\nMY PROGRESS")
    print("9.  Exercise Progress")
    print("10. Personal Records")
    print("11. Progress Leaderboard")
    print("12. Progress Watch")
    print("13. Weekly Forge Report")
    print("\nSETTINGS")
    print("14. My Goals")
    print("\n0.  Exit")
    line("=")


def exercise_label(exercise: dict) -> str:
    return f"{exercise['name']} ({exercise['muscle_group']})"


def select_exercise():
    exercises = get_exercises()
    return choose_from_list(exercises, "SELECT EXERCISE", exercise_label)


def display_previous_performance(exercise_name: str, workouts: list[dict]):
    previous = get_previous_performance(workouts, exercise_name)
    personal_best = get_personal_best(workouts, exercise_name)

    print()
    line()
    print(exercise_name.upper())
    line()

    if previous is None:
        print("No previous performance recorded.")
        print("This will become your first ProgressForge record.")
        return None

    print("Last session:", format_date(previous.get("date", "")))
    print(f"Weight: {to_float(previous.get('weight')):.1f} kg")
    print(f"Sets:   {to_int(previous.get('sets'))}")
    print(f"Reps:   {to_int(previous.get('reps'))}")
    print(f"Volume: {to_float(previous.get('volume')):.1f} kg")

    if personal_best:
        print(f"\nCurrent personal best: {to_float(personal_best.get('weight')):.1f} kg")

    return previous


def display_session_comparison(previous, current: dict):
    comparison = compare_performances(previous, current)

    heading("SESSION COMPARISON")
    if not comparison["has_previous"]:
        print("First record saved for this exercise.")
        print(f"Training volume: {comparison['current_volume']:.1f} kg")
        return

    print(f"Previous weight: {comparison['previous_weight']:.1f} kg")
    print(f"Current weight:  {comparison['current_weight']:.1f} kg")
    print(f"Weight change:   {comparison['weight_change']:+.1f} kg")
    if comparison["weight_change_percent"] is not None:
        print(f"Weight change:   {comparison['weight_change_percent']:+.1f}%")

    print()
    print(f"Previous volume: {comparison['previous_volume']:.1f} kg")
    print(f"Current volume:  {comparison['current_volume']:.1f} kg")
    print(f"Volume change:   {comparison['volume_change']:+.1f} kg")
    if comparison["volume_change_percent"] is not None:
        print(f"Volume change:   {comparison['volume_change_percent']:+.1f}%")

    print(f"\nResult: {comparison['result']}.")


def log_one_exercise(exercise: dict, routine_name: str = "Quick Log"):
    workouts = get_workouts()
    exercise_name = exercise["name"]
    previous = display_previous_performance(exercise_name, workouts)

    print("\nEnter today's performance")
    sets = get_positive_int("Sets: ")
    reps = get_positive_int("Reps per set: ")
    weight = get_positive_float("Weight in kg: ")
    volume = calculate_volume(sets, reps, weight)

    new_pr, previous_best_weight = is_new_personal_record(workouts, exercise_name, weight)

    record = {
        "date": date.today().isoformat(),
        "routine": routine_name,
        "exercise": exercise_name,
        "sets": sets,
        "reps": reps,
        "weight": round(weight, 2),
        "volume": volume,
    }
    add_workout(record)

    print("\nWorkout record saved.")
    print(f"Training volume: {volume:.1f} kg")
    display_session_comparison(previous, record)

    if previous_best_weight is None:
        print(f"\nInitial personal best established: {weight:.1f} kg")
    elif new_pr:
        heading("NEW PERSONAL RECORD")
        print(exercise_name)
        improvement = ((weight - previous_best_weight) / previous_best_weight) * 100
        print(f"Previous best: {previous_best_weight:.1f} kg")
        print(f"New best:      {weight:.1f} kg")
        print(f"Improvement:   {improvement:+.1f}%")


def start_today_workout():
    heading("START TODAY'S WORKOUT")
    routines = get_routines()
    routine_names = list(routines.keys()) + ["Custom Session"]
    selected = choose_from_list(routine_names, "SELECT ROUTINE")
    if selected is None:
        return

    exercises = get_exercises()
    exercise_lookup = {item["name"]: item for item in exercises}

    if selected == "Custom Session":
        chosen_exercises = []
        print("\nSelect exercises one at a time. Choose 0 when finished.")
        while True:
            exercise = choose_from_list(exercises, "CUSTOM SESSION", exercise_label)
            if exercise is None:
                break
            if exercise not in chosen_exercises:
                chosen_exercises.append(exercise)
                print(f"Added: {exercise['name']}")
            else:
                print("That exercise is already in this session.")
        routine_exercises = chosen_exercises
    else:
        routine_exercises = []
        for exercise_name in routines[selected]:
            exercise = exercise_lookup.get(exercise_name)
            if exercise:
                routine_exercises.append(exercise)

    if not routine_exercises:
        print("No exercises selected.")
        return

    print(f"\nToday's routine: {selected}")
    for exercise in routine_exercises:
        print(f"- {exercise['name']}")

    start = input("\nStart this workout? (y/n): ").strip().lower()
    if start != "y":
        print("Workout cancelled.")
        return

    completed = 0
    for exercise in routine_exercises:
        answer = input(f"\nLog {exercise['name']} now? (Y/n): ").strip().lower()
        if answer in ("", "y"):
            log_one_exercise(exercise, selected)
            completed += 1
        else:
            print(f"Skipped {exercise['name']}.")

    print(f"\nSession complete: {completed}/{len(routine_exercises)} exercises recorded.")


def quick_log_exercise():
    heading("QUICK LOG EXERCISE")
    exercise = select_exercise()
    if exercise:
        log_one_exercise(exercise)


def exercise_vault_menu():
    while True:
        heading("MY EXERCISE VAULT")
        exercises = get_exercises()
        for index, exercise in enumerate(exercises, start=1):
            print(
                f"{index:>2}. {exercise['name']} | {exercise['muscle_group']} | "
                f"{exercise['equipment']} | usual sets: {exercise['usual_sets']}"
            )

        print("\n1. Add Exercise")
        print("0. Back")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            return
        if choice != "1":
            print("Invalid choice.")
            continue

        name = input("Exercise name: ").strip()
        if not name:
            print("Exercise name cannot be empty.")
            continue

        duplicate = any(item["name"].lower() == name.lower() for item in exercises)
        if duplicate:
            print("That exercise already exists in your vault.")
            continue

        muscle_group = input("Muscle group: ").strip() or "Other"
        equipment = input("Equipment: ").strip() or "Not specified"
        usual_sets = get_positive_int("Usual number of sets: ")
        note = input("Optional personal note: ").strip()

        exercises.append(
            {
                "name": name,
                "muscle_group": muscle_group,
                "equipment": equipment,
                "usual_sets": usual_sets,
                "note": note,
            }
        )
        save_exercises(exercises)
        print(f"Added {name} to My Exercise Vault.")


def routines_menu():
    while True:
        heading("MY ROUTINES")
        routines = get_routines()
        for name, exercises in routines.items():
            print(f"\n{name}")
            if exercises:
                for exercise in exercises:
                    print(f"  - {exercise}")
            else:
                print("  (No exercises yet)")

        print("\n1. Create Routine")
        print("2. Add Exercise to Routine")
        print("0. Back")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            return

        if choice == "1":
            name = input("New routine name: ").strip()
            if not name:
                print("Routine name cannot be empty.")
                continue
            if name in routines:
                print("That routine already exists.")
                continue
            routines[name] = []
            save_routines(routines)
            print(f"Created routine: {name}")

        elif choice == "2":
            routine_name = choose_from_list(list(routines.keys()), "SELECT ROUTINE")
            if routine_name is None:
                continue
            exercise = select_exercise()
            if exercise is None:
                continue
            if exercise["name"] in routines[routine_name]:
                print("That exercise is already in this routine.")
                continue
            routines[routine_name].append(exercise["name"])
            save_routines(routines)
            print(f"Added {exercise['name']} to {routine_name}.")
        else:
            print("Invalid choice.")


def show_workout_history():
    heading("WORKOUT HISTORY")
    workouts = get_workouts()
    if not workouts:
        print("No workout history recorded yet.")
        return

    print("Showing most recent records:\n")
    for record in workouts[-20:][::-1]:
        print(
            f"{format_date(record.get('date', '')):<12} | "
            f"{record.get('routine', ''):<12} | "
            f"{record.get('exercise', ''):<25} | "
            f"{to_int(record.get('sets'))}x{to_int(record.get('reps'))} @ "
            f"{to_float(record.get('weight')):.1f} kg | "
            f"Vol {to_float(record.get('volume')):.1f}"
        )


def show_training_memory():
    heading("TRAINING MEMORY")
    exercise = select_exercise()
    if exercise is None:
        return

    analysis = analyse_exercise_progress(get_workouts(), exercise["name"])
    if analysis is None:
        print("No training records exist for this exercise yet.")
        return

    print(f"\n{exercise['name'].upper()} - TRAINING MEMORY")
    line()
    for record in analysis["records"]:
        print(
            f"{format_date(record.get('date', '')):<12} "
            f"{to_float(record.get('weight')):>6.1f} kg  "
            f"{to_int(record.get('reps')):>2} reps  "
            f"{to_int(record.get('sets')):>2} sets  "
            f"volume {to_float(record.get('volume')):>7.1f}"
        )

    print()
    print(f"First recorded weight: {analysis['first_weight']:.1f} kg")
    print(f"Latest weight:         {analysis['latest_weight']:.1f} kg")
    print(f"Highest weight:        {analysis['highest_weight']:.1f} kg")
    print(f"Overall change:        {analysis['weight_change']:+.1f} kg")
    if analysis["weight_change_percent"] is not None:
        print(f"Percentage change:     {analysis['weight_change_percent']:+.1f}%")
    print(f"Sessions recorded:     {analysis['sessions_recorded']}")


def show_exercise_progress():
    heading("EXERCISE PROGRESS")
    exercise = select_exercise()
    if exercise is None:
        return

    analysis = analyse_exercise_progress(get_workouts(), exercise["name"])
    if analysis is None:
        print("No records exist for this exercise yet.")
        return

    print(f"\nExercise: {exercise['name']}")
    line()
    print(f"First weight:          {analysis['first_weight']:.1f} kg")
    print(f"Latest weight:         {analysis['latest_weight']:.1f} kg")
    print(f"Highest weight:        {analysis['highest_weight']:.1f} kg")
    print(f"Weight change:         {analysis['weight_change']:+.1f} kg")
    if analysis["weight_change_percent"] is not None:
        print(f"Weight change:         {analysis['weight_change_percent']:+.1f}%")
    print()
    print(f"First volume:          {analysis['first_volume']:.1f} kg")
    print(f"Latest volume:         {analysis['latest_volume']:.1f} kg")
    print(f"Volume change:         {analysis['volume_change']:+.1f} kg")
    if analysis["volume_change_percent"] is not None:
        print(f"Volume change:         {analysis['volume_change_percent']:+.1f}%")
    print(f"Sessions recorded:     {analysis['sessions_recorded']}")
    print("\nNote: training volume is a simple sets x reps x weight metric, not a medical or scientific diagnosis.")


def show_personal_records():
    heading("PERSONAL RECORDS")
    records = personal_records(get_workouts())
    if not records:
        print("No workout records are available yet.")
        return

    for record in records:
        print(
            f"{record['exercise']:<28} {record['weight']:>6.1f} kg  "
            f"({record['sets']}x{record['reps']}, {format_date(record['date'])})"
        )
    print("\nPR rule: highest recorded weight for each exercise.")


def show_progress_leaderboard():
    heading("MY PROGRESS LEADERBOARD")
    results = progress_leaderboard(get_workouts())
    if not results:
        print("At least two records for an exercise are needed before it can be ranked.")
        return

    for index, result in enumerate(results, start=1):
        print(f"{index:>2}. {result['exercise']:<28} {result['change_percent']:+.1f}%")
    print("\nRanking uses first-to-latest recorded working-weight percentage change.")


def show_progress_watch():
    heading("PROGRESS WATCH")
    workouts = get_workouts()
    exercises = get_exercises()
    found_history = False

    for exercise in exercises:
        result = progress_watch_status(workouts, exercise["name"])
        if result["recent_records"]:
            found_history = True
            change = result.get("change_percent")
            change_text = f" ({change:+.1f}% volume)" if change is not None else ""
            print(f"{exercise['name']:<30} {result['status']}{change_text}")

    if not found_history:
        print("No workout history is available yet.")
    else:
        print("\nRules use the last three recorded training-volume values.")
        print("This is descriptive progress tracking, not a scientific plateau diagnosis.")


def record_body_weight():
    heading("RECORD BODY WEIGHT")
    weight = get_positive_float("Today's body weight in kg: ")
    add_bodyweight({"date": date.today().isoformat(), "weight": round(weight, 2)})
    print("Body-weight record saved.")

    analysis = analyse_bodyweight(get_bodyweights())
    if analysis:
        print("\nBODY WEIGHT SUMMARY")
        line()
        print(f"First recorded:        {analysis['first_weight']:.1f} kg")
        print(f"Latest recorded:       {analysis['latest_weight']:.1f} kg")
        print(f"Total change:          {analysis['total_change']:+.1f} kg")
        if analysis["total_change_percent"] is not None:
            print(f"Percentage change:     {analysis['total_change_percent']:+.1f}%")
        print(f"Current 7-day avg:     {analysis['current_7_average']:.2f} kg")
        if analysis["previous_7_average"] is not None:
            print(f"Previous 7-day avg:   {analysis['previous_7_average']:.2f} kg")
        else:
            print("Previous 7-day avg:   Not enough earlier entries")
        print("\nThis is descriptive tracking only; it does not provide medical advice.")


def record_nutrition():
    heading("RECORD NUTRITION")
    calories = get_positive_float("Today's calories: ")
    protein = get_positive_float("Today's protein in grams: ")
    add_nutrition(
        {
            "date": date.today().isoformat(),
            "calories": round(calories, 1),
            "protein": round(protein, 1),
        }
    )
    print("Nutrition record saved.")

    settings = get_settings()
    analysis = analyse_nutrition(
        get_nutrition(),
        float(settings["daily_protein_target"]),
        float(settings["daily_calorie_target"]),
    )
    if analysis:
        print("\nNUTRITION SUMMARY")
        line()
        print(f"Average calories:      {analysis['average_calories']:.0f}")
        print(f"Personal calorie target: {analysis['calorie_target']:.0f}")
        print(f"Average protein:       {analysis['average_protein']:.1f} g")
        print(f"Personal protein target: {analysis['protein_target']:.1f} g")
        print(f"Protein target reached: {analysis['days_protein_target']}/{analysis['entries']} recorded days")
        print(f"Average difference:    {analysis['protein_difference']:+.1f} g")
        print("\nTargets are personal settings, not universal medical recommendations.")


def show_weekly_forge_report():
    heading("PROGRESSFORGE WEEKLY REPORT")
    report = weekly_report(
        get_workouts(),
        get_bodyweights(),
        get_nutrition(),
        get_settings(),
    )

    print(f"Period: {report['current_start'].strftime('%d %b %Y')} - {report['current_end'].strftime('%d %b %Y')}")

    print("\nTRAINING")
    line()
    print(f"Sessions completed:         {report['current_sessions']}")
    print(f"Weekly personal target:     {report['weekly_target']}")
    if report["completion_percent"] is not None:
        print(f"Completion:                 {report['completion_percent']:.1f}%")

    print("\nSTRENGTH")
    line()
    print(f"Exercises improved:         {report['exercises_improved']}")
    print(f"Exercises stable/not up:    {report['exercises_stable']}")
    print(f"New personal records:       {report['personal_records']}")

    print("\nBEST PROGRESS")
    line()
    if report["best_progress"]:
        best = report["best_progress"]
        print(best["exercise"])
        print(f"Previous:                   {best['previous_weight']:.1f} kg")
        print(f"Current:                    {best['current_weight']:.1f} kg")
        print(f"Change:                     {best['change_percent']:+.1f}%")
    else:
        print("Not enough comparable exercise history this period.")

    print("\nTRAINING VOLUME")
    line()
    print(f"Previous 7 days:            {report['previous_volume']:.1f} kg")
    print(f"Current 7 days:             {report['current_volume']:.1f} kg")
    if report["volume_change_percent"] is not None:
        print(f"Change:                     {report['volume_change_percent']:+.1f}%")
    else:
        print("Change:                     Not available")

    print("\nBODY WEIGHT")
    line()
    if report["current_bw_average"] is None:
        print("No body-weight records in this period.")
    else:
        print(f"Current period average:     {report['current_bw_average']:.2f} kg")
        if report["previous_bw_average"] is not None:
            print(f"Previous period average:    {report['previous_bw_average']:.2f} kg")
            print(f"Average change:             {report['bodyweight_change']:+.2f} kg")
        else:
            print("Previous period average:    Not enough data")

    print("\nNUTRITION")
    line()
    if report["average_protein"] is None:
        print("No nutrition records in this period.")
    else:
        print(f"Protein target:             {report['protein_target']:.1f} g")
        print(f"Average protein:            {report['average_protein']:.1f} g")
        print(f"Target achieved:            {report['protein_target_days']}/{report['nutrition_days']} recorded days")

    print("\nPROGRESSFORGE SUMMARY")
    line()
    for sentence in report["summary"]:
        print(f"- {sentence}")
    print("\nThe report describes recorded data and supports your own judgement; it is not medical advice.")


def goals_menu():
    while True:
        heading("MY GOALS")
        settings = get_settings()
        print(f"1. Weekly workout target: {settings['weekly_workout_target']} sessions")
        print(f"2. Daily protein target:  {settings['daily_protein_target']} g")
        print(f"3. Daily calorie target:  {settings['daily_calorie_target']} kcal")
        print(f"4. Body-weight goal:      {settings['bodyweight_goal']} kg")
        print("0. Back")

        choice = input("Choose a goal to update: ").strip()
        if choice == "0":
            return
        if choice == "1":
            settings["weekly_workout_target"] = get_optional_positive_int(
                f"New weekly target [{settings['weekly_workout_target']}]: ",
                int(settings["weekly_workout_target"]),
            )
        elif choice == "2":
            settings["daily_protein_target"] = get_optional_positive_float(
                f"New protein target [{settings['daily_protein_target']}]: ",
                float(settings["daily_protein_target"]),
            )
        elif choice == "3":
            settings["daily_calorie_target"] = get_optional_positive_float(
                f"New calorie target [{settings['daily_calorie_target']}]: ",
                float(settings["daily_calorie_target"]),
            )
        elif choice == "4":
            settings["bodyweight_goal"] = get_optional_positive_float(
                f"New body-weight goal [{settings['bodyweight_goal']}]: ",
                float(settings["bodyweight_goal"]),
            )
        else:
            print("Invalid choice.")
            continue

        save_settings(settings)
        print("Goal updated.")


def main():
    ensure_data_files()

    while True:
        display_main_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("\nThanks for using ProgressForge. Keep progressing!")
            break
        elif choice == "1":
            start_today_workout()
        elif choice == "2":
            quick_log_exercise()
        elif choice == "3":
            record_body_weight()
        elif choice == "4":
            record_nutrition()
        elif choice == "5":
            exercise_vault_menu()
        elif choice == "6":
            routines_menu()
        elif choice == "7":
            show_workout_history()
        elif choice == "8":
            show_training_memory()
        elif choice == "9":
            show_exercise_progress()
        elif choice == "10":
            show_personal_records()
        elif choice == "11":
            show_progress_leaderboard()
        elif choice == "12":
            show_progress_watch()
        elif choice == "13":
            show_weekly_forge_report()
        elif choice == "14":
            goals_menu()
        else:
            print("\nInvalid choice. Please choose a number shown in the menu.")
            continue

        pause()


if __name__ == "__main__":
    main()
