"""Configuration values and file paths for ProgressForge."""

from pathlib import Path

APP_NAME = "ProgressForge"
APP_TAGLINE = "My Training Memory & Progress Engine"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_DATA_DIR = BASE_DIR / "sample-data"

EXERCISES_FILE = DATA_DIR / "exercises.json"
ROUTINES_FILE = DATA_DIR / "routines.json"
WORKOUTS_FILE = DATA_DIR / "workouts.csv"
BODYWEIGHT_FILE = DATA_DIR / "bodyweight.csv"
NUTRITION_FILE = DATA_DIR / "nutrition.csv"
SETTINGS_FILE = DATA_DIR / "settings.json"

WORKOUT_FIELDS = ["date", "routine", "exercise", "sets", "reps", "weight", "volume"]
BODYWEIGHT_FIELDS = ["date", "weight"]
NUTRITION_FIELDS = ["date", "calories", "protein"]

DEFAULT_EXERCISES = [
    {
        "name": "Incline Dumbbell Press",
        "muscle_group": "Chest",
        "equipment": "Dumbbells",
        "usual_sets": 3,
        "note": "Main upper-chest press",
    },
    {
        "name": "Machine Chest Press",
        "muscle_group": "Chest",
        "equipment": "Machine",
        "usual_sets": 3,
        "note": "Stable pressing movement",
    },
    {
        "name": "Cable Fly",
        "muscle_group": "Chest",
        "equipment": "Cable",
        "usual_sets": 3,
        "note": "Controlled chest isolation",
    },
    {
        "name": "Lat Pulldown",
        "muscle_group": "Back",
        "equipment": "Cable",
        "usual_sets": 3,
        "note": "Main vertical pulling movement",
    },
    {
        "name": "Seated Cable Row",
        "muscle_group": "Back",
        "equipment": "Cable",
        "usual_sets": 3,
        "note": "Main horizontal pulling movement",
    },
    {
        "name": "Chest-Supported Row",
        "muscle_group": "Back",
        "equipment": "Machine or dumbbells",
        "usual_sets": 3,
        "note": "Back-focused row with chest support",
    },
    {
        "name": "Dumbbell Shoulder Press",
        "muscle_group": "Shoulders",
        "equipment": "Dumbbells",
        "usual_sets": 3,
        "note": "Main shoulder press",
    },
    {
        "name": "Lateral Raise",
        "muscle_group": "Shoulders",
        "equipment": "Dumbbells or cable",
        "usual_sets": 3,
        "note": "Side-delt isolation",
    },
    {
        "name": "Dumbbell Curl",
        "muscle_group": "Arms",
        "equipment": "Dumbbells",
        "usual_sets": 3,
        "note": "Biceps exercise",
    },
    {
        "name": "Tricep Pushdown",
        "muscle_group": "Arms",
        "equipment": "Cable",
        "usual_sets": 3,
        "note": "Triceps exercise",
    },
    {
        "name": "Leg Press",
        "muscle_group": "Legs",
        "equipment": "Machine",
        "usual_sets": 3,
        "note": "Main lower-body pressing movement",
    },
    {
        "name": "Leg Extension",
        "muscle_group": "Legs",
        "equipment": "Machine",
        "usual_sets": 3,
        "note": "Quadriceps isolation",
    },
    {
        "name": "Hamstring Curl",
        "muscle_group": "Legs",
        "equipment": "Machine",
        "usual_sets": 3,
        "note": "Hamstring isolation",
    },
]

DEFAULT_ROUTINES = {
    "Chest": [
        "Incline Dumbbell Press",
        "Machine Chest Press",
        "Cable Fly",
        "Tricep Pushdown",
    ],
    "Back": [
        "Lat Pulldown",
        "Seated Cable Row",
        "Chest-Supported Row",
        "Dumbbell Curl",
    ],
    "Shoulders": [
        "Dumbbell Shoulder Press",
        "Lateral Raise",
        "Tricep Pushdown",
    ],
    "Arms": [
        "Dumbbell Curl",
        "Tricep Pushdown",
        "Lateral Raise",
    ],
    "Legs": [
        "Leg Press",
        "Leg Extension",
        "Hamstring Curl",
    ],
}

DEFAULT_SETTINGS = {
    "weekly_workout_target": 5,
    "daily_protein_target": 130,
    "daily_calorie_target": 2500,
    "bodyweight_goal": 70.0,
}
