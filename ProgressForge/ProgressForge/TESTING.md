# ProgressForge Testing Report

Date of build testing: **22 September 2026**

The generated build was actually executed during development. Tests that required populated history used a separate copy of the project with the fictional files in `02-project/sample-data/`, so the blank personal-data files in the final package were not contaminated.

## Environment used for build verification

- Python 3.13 in the build environment
- Python standard library only
- No external packages

The student should repeat the important manual tests on the final Windows + Visual Studio Code environment before submission.

## Executed checks

| Area | Test performed | Result |
|---|---|---|
| Syntax | Compiled `main.py`, `storage.py`, `analytics.py`, `config.py` with `py_compile` | PASS |
| Startup | Ran `python main.py` | PASS |
| Menu | Main menu displayed | PASS |
| Exit | Entered `0` | PASS |
| Empty data | Opened Weekly Forge Report with blank CSV files | PASS |
| Missing file | Deleted a test-copy `workouts.csv`, ran data initialisation, checked file/header recreated | PASS |
| Exercise Vault | Added a fictional `Test Exercise` in the test copy | PASS |
| Goals | Changed weekly workout target from 5 to 6 in the test copy | PASS |
| Quick Log | Logged Incline Dumbbell Press using sample history | PASS |
| Previous performance | Previous 24 kg Incline Dumbbell Press record displayed before logging | PASS |
| Session comparison | Compared 24 kg previous record with a new 25 kg test record | PASS |
| PR detection | New 25 kg highest-weight PR detected | PASS |
| Invalid sets | Entered `hello` then a valid number | PASS |
| Invalid reps | Entered `0` then a valid number | PASS |
| Invalid weight | Entered `-2` then a valid number | PASS |
| Training Memory | Displayed Lat Pulldown history from sample data | PASS |
| Progress Watch | Produced transparent statuses from recent sample volumes | PASS |
| Body weight | Added a test entry and displayed rolling 7-day summary | PASS |
| Nutrition | Added a test entry and displayed nutrition summary | PASS |
| Weekly report | Generated report using current and previous seven-day sample records | PASS |
| Analytics | Asserted training volume, percentage change, leaderboard, body-weight averages, and weekly report values | PASS |

## Verified analytics values from sample data

- `3 × 10 × 24 kg` training volume = **720 kg**
- `20 kg → 24 kg` percentage change = **20.0%**
- Lat Pulldown sample history: **45.0 kg → 50.0 kg**, **+11.1%**
- Sample current 7-day body-weight average = **67.81 kg**
- Sample previous 7-day body-weight average = **67.21 kg**
- Sample Weekly Forge Report sessions = **4**
- Sample Weekly Forge Report target completion = **80.0%**
- Sample current training volume = **8508.0 kg**
- Sample previous training volume = **7773.0 kg**
- Sample current average protein = **131.6 g**

## Manual tests to repeat locally before submission

### Application
- [ ] Run from the official repository root.
- [ ] Main menu appears without import/path errors.
- [ ] Invalid menu choice does not crash the program.
- [ ] Exit works.

### Exercise Vault
- [ ] Starter exercises load.
- [ ] Add one temporary exercise.
- [ ] Duplicate exercise name is rejected.
- [ ] Remove the temporary test exercise manually afterward if it is not wanted.

### Routines
- [ ] Starter routines display.
- [ ] Create one temporary routine.
- [ ] Add one vault exercise to it.
- [ ] Confirm the routine persists after restarting.

### Workout logging
- [ ] Log an exercise with no prior history.
- [ ] Restart the application.
- [ ] Log the same exercise again.
- [ ] Confirm previous performance is displayed.
- [ ] Confirm the second record persists in `workouts.csv`.

### Validation
- [ ] Enter text for sets.
- [ ] Enter `0` for reps.
- [ ] Enter a negative weight.
- [ ] Confirm the program asks again instead of crashing.

### PR detection
- [ ] First record becomes initial best.
- [ ] Equal weight does not count as a new PR.
- [ ] Higher weight counts as a new PR.

### Training Memory and analytics
- [ ] No-history message works.
- [ ] One-record history works.
- [ ] Multiple records display in date order.
- [ ] Percentage change matches a manual calculation.
- [ ] Training volume matches `sets × reps × weight`.
- [ ] Progress Leaderboard excludes exercises with insufficient history.
- [ ] Progress Watch explains that it uses the last three volume records.

### Body weight
- [ ] First entry saves.
- [ ] Several entries save.
- [ ] Current 7-day average appears.
- [ ] Previous 7-day average only appears when earlier dated records exist.

### Nutrition
- [ ] Calories and protein save.
- [ ] Personal target comparison displays.
- [ ] Empty nutrition history is handled in Weekly Forge Report.

### Weekly Forge Report
- [ ] Works with no data.
- [ ] Works with partial data.
- [ ] Works with training + body-weight + nutrition data.
- [ ] Seven-day period shown is correct for the day of demonstration.

## Important testing note

Passing tests does not mean the software provides scientific fitness advice. Testing verifies that the program's own documented rules and calculations behave as intended.
