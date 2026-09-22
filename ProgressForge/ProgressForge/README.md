# ProgressForge — My Training Memory & Progress Engine

ProgressForge is a personal command-line Python program created for ISYS5002 Introduction to Programming. It is designed around a small set of exercises and routines that I perform regularly, rather than trying to become a large general-purpose fitness platform.

Its main question is:

> **Am I actually progressing in the exercises that I personally perform regularly?**

The program records training data, remembers previous performances, calculates simple training volume, detects highest-weight personal records, compares sessions, and produces progress summaries. Body weight and nutrition are included as supporting information.

## Rationale

It is easy to remember that I trained, but harder to remember exactly what weight, sets and reps I used several sessions ago. ProgressForge gives me a consistent place to record those repeated exercises and turns the history into simple comparisons that I can use when deciding what to do next.

The program is intentionally personal. It begins with a small **Exercise Vault** and personal routines rather than a database containing hundreds of exercises.

## Main features

- Personal Exercise Vault
- Personal routines
- Start Today's Workout workflow
- Quick Log Exercise
- Previous-performance reminder
- Simple training volume: `sets × reps × weight`
- Session comparison
- Highest-weight personal-record detection
- Training Memory for each exercise
- Exercise Progress summary
- Progress Leaderboard
- Progress Watch using the last three recorded volumes
- Body-weight recording and rolling 7-day averages
- Simple calorie/protein recording
- Personal goals stored in JSON
- Weekly Forge Report combining training, body weight and nutrition
- Input validation and empty-data handling

## Project structure

```text
02-project/
├── main.py
├── storage.py
├── analytics.py
├── config.py
├── data/
│   ├── exercises.json
│   ├── routines.json
│   ├── workouts.csv
│   ├── bodyweight.csv
│   ├── nutrition.csv
│   └── settings.json
└── sample-data/
    ├── exercises_sample.json
    ├── routines_sample.json
    ├── workouts_sample.csv
    ├── bodyweight_sample.csv
    ├── nutrition_sample.csv
    └── settings_sample.json
```

`main.py` manages the command-line interface and user choices.

`storage.py` reads and writes CSV/JSON data.

`analytics.py` contains the calculations used for comparisons and reports.

`config.py` stores project paths, CSV headings, starter exercises, starter routines and default goals.

## Requirements

- Python 3
- No external Python packages are required

ProgressForge uses only Python standard-library modules including `csv`, `json`, `datetime`, `statistics` and `pathlib`.

## How to run

From the root of the official repository:

```bash
python 02-project/main.py
```

On some Windows installations, use:

```bash
py 02-project/main.py
```

The program creates missing local data files automatically when it starts.

## How to use

1. Open ProgressForge.
2. Review **My Exercise Vault** and **My Routines**.
3. Choose **Start Today's Workout** for a routine or **Quick Log Exercise** for one exercise.
4. ProgressForge shows the most recent performance before asking for the new performance.
5. Enter sets, reps and weight.
6. The program saves the result and compares it with the previous session.
7. Use **Training Memory**, **Exercise Progress**, **Personal Records**, **Progress Leaderboard** and **Progress Watch** to review the history.
8. Record body weight and nutrition if desired.
9. Use **Weekly Forge Report** for a seven-day summary.

## Data storage

Training, body-weight and nutrition records use CSV because the files are simple, human-readable and suitable for tabular records.

Exercises, routines and personal goals use JSON because these values are naturally represented as lists and dictionaries.

Workout records use the following columns:

```text
date,routine,exercise,sets,reps,weight,volume
```

Dates use ISO format (`YYYY-MM-DD`).

## Training-volume calculation

ProgressForge uses this simple calculation:

```text
training volume = sets × reps × weight
```

This is useful for comparing recorded sessions, but it is a simplified metric. It does not account for exercise technique, range of motion, effort, rest time or many other factors that influence training.

## Personal-record rule

For ProgressForge V1, a personal record means the **highest recorded weight for an exercise**. The first recorded performance becomes the initial best. A later performance is marked as a new personal record only when its recorded weight is higher than the previous highest weight.

## Progress Watch rules

Progress Watch examines the last three recorded training-volume values for an exercise:

- fewer than three records → `NOT ENOUGH DATA`
- latest volume more than 2% above the first of the three → `IMPROVING`
- latest volume more than 2% below the first of the three → `RECENT DECREASE`
- all three volumes equal → `NO RECENT CHANGE`
- otherwise → `STABLE`

These are transparent program rules, not scientific predictions or medical conclusions.

## Privacy design

Real workout history, body-weight records, nutrition records and personal goal settings are local personal data. The supplied `.gitignore` therefore excludes:

- `02-project/data/workouts.csv`
- `02-project/data/bodyweight.csv`
- `02-project/data/nutrition.csv`
- `02-project/data/settings.json`

Safe fictional sample data is stored separately under `02-project/sample-data/` for demonstrations and testing.

If a data file is already tracked by Git before `.gitignore` is added, Git will continue tracking it until it is explicitly untracked. This should be checked before pushing personal data.

## Sociotechnical considerations

### 1. Privacy-aware separation of source code and personal records

ProgressForge separates program logic from personal training records. Personal CSV files are excluded from Git by default, while fictional sample files are available for demonstration. This reduces the chance that personal records are accidentally published or submitted with source code.

### 2. Decision support rather than professional advice

ProgressForge reports recorded values and transparent comparisons. It does not claim to diagnose training plateaus, prescribe medical treatment, or decide whether a workout or nutrition target is safe. Protein, calorie, workout and body-weight targets are user-configured personal settings. The final judgement remains with the user.

## External packages and open-source acknowledgements

ProgressForge currently uses **no external Python packages**. No `pip install` command is required.

The program uses Python standard-library modules only.

## AI assistance

Generative AI was used during the development process. AI-assisted work must be recorded honestly using the ISYS5002 AI-assistance record-keeping process. Relevant conversations should be stored in the official repository's `ai-assistance-logs` folder and committed alongside the corresponding code changes where required by the unit specification.

AI use does not remove the student's responsibility to understand, test and explain the submitted code.

## Research inspiration

During planning, several open-source fitness projects were reviewed as research references for ideas such as exercise organisation, workout logging, progression, reporting and code separation:

- Snouzy/workout-cool
- KenAli77/InFit
- CodeWithCJ/SparkyFitness
- wger-project/wger
- ThreeDotsLabs/wild-workouts-go-ddd-example
- hasaneyldrm/exercises-dataset

Their source code was not copied into ProgressForge. ProgressForge uses its own Python implementation and deliberately focuses on a small personal training workflow rather than reproducing a large fitness platform.

## Limitations

- Results depend on the accuracy and consistency of user input.
- Training volume is a simplified comparison metric.
- A highest-weight PR does not capture every type of performance improvement.
- Progress Watch uses only the last three recorded volume values and is not a scientific prediction.
- Weekly statistics are based only on records entered into ProgressForge.
- Body-weight and nutrition summaries are descriptive and are not medical advice.
- ProgressForge is a local command-line application and does not synchronise with wearables or online services.

## Safe demonstration data

The `sample-data` folder contains fictional records. They are intended only for testing and demonstrating program behaviour. They must not be represented as real personal training history.

## Assessment reminder

Before submission, verify the official assessment specification, README requirements, AI logs, Git history, Blackboard uploads, video requirements and live demonstration requirements. The code should only be submitted after the student can explain the major functions and design decisions.
