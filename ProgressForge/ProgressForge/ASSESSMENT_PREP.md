# ProgressForge Assessment Preparation

This is a development-support file, not a replacement for the official ISYS5002 assessment specification.

## Suggested Git milestone plan

Only create commits after the corresponding work actually exists. Do not fabricate historical commits.

Possible meaningful commits for the current codebase if you develop/transfer it in stages:

1. `[AI-assisted] [feat] initialise ProgressForge CLI and project structure`
2. `[AI-assisted] [feat] add exercise vault and personal routines`
3. `[AI-assisted] [feat] implement workout logging and CSV storage`
4. `[AI-assisted] [feat] add previous-performance comparison and PR detection`
5. `[AI-assisted] [feat] add training memory and exercise progress analytics`
6. `[AI-assisted] [feat] add progress leaderboard and progress watch`
7. `[AI-assisted] [feat] add body-weight nutrition and personal goals`
8. `[AI-assisted] [feat] generate weekly forge report`
9. `[AI-assisted] [docs] add README privacy notes and testing report`
10. `[AI-assisted] [fix] final validation and assessment cleanup`

Use the exact AI attribution/record-keeping format required by your unit guidance. The suggestions above are not permission to back-date commits.

Typical local commands after a real development step:

```bash
git status
git add 02-project README.md TESTING.md
git add ai-assistance-logs/<the-real-log-file>.md
git commit -m "[AI-assisted] [feat] describe the real change"
git push
```

Check `git status` before every commit so personal CSV data is not staged accidentally.

## AI assistance log plan

- Save the real ChatGPT conversation(s) that materially influenced the code.
- Keep user prompts and AI responses accurate and in order.
- Do not create fake conversations later.
- Keep each log aligned with the code change it actually influenced.
- Follow the exact filename and commit rules demonstrated in ISYS5002.
- Be ready to explain which parts were AI-assisted and what you personally tested/understood.

## Five-minute video plan

Follow the official assessment timing/requirements rather than treating this as a new rubric.

### 1. Personal story — about 1 minute

Explain the genuine problem:

- you repeat many of the same gym exercises;
- remembering the last weight/reps/sets is difficult;
- a generic exercise database is not the main goal;
- ProgressForge is built around your own repeated training and progress decisions.

### 2. Product demonstration — about 1 minute

Use a short, reliable path:

1. Launch ProgressForge.
2. Start Today's Workout or Quick Log Exercise.
3. Select a familiar exercise.
4. Show previous performance.
5. Enter a new performance.
6. Show session comparison / PR if available.
7. Briefly open Training Memory or Weekly Forge Report.

Do not spend this section reading source code line by line.

### 3. Python explanation — about 3 minutes

Show the separation of responsibilities:

- `main.py`: menu and user interaction
- `storage.py`: CSV/JSON reading and writing
- `analytics.py`: calculations
- `config.py`: paths/default values

Strong functions to explain:

- `calculate_volume()`
- `percentage_change()`
- `get_previous_performance()`
- `is_new_personal_record()`
- `progress_watch_status()`
- `weekly_report()`

Mention that simple transparent rules were chosen so results remain understandable and explainable.

## Likely live-demonstration questions and short answers

**Why this project?**  
I regularly repeat the same exercises and wanted a personal way to remember previous performance and see whether my recorded training is changing over time.

**Why CSV?**  
Workout, body-weight and nutrition records are tabular. CSV is simple, human-readable and can be handled with Python's standard `csv` module.

**Why JSON?**  
Exercises, routines and goals are naturally lists/dictionaries, so JSON stores that structure clearly.

**What does `main.py` do?**  
It runs the CLI, gets user choices and calls the appropriate storage or analytics functions.

**What does `storage.py` do?**  
It creates, reads and writes the CSV/JSON files so file handling is not mixed throughout the menu code.

**What does `analytics.py` do?**  
It performs calculations such as training volume, percentage change, PR checks, progress summaries and weekly reporting.

**How is training volume calculated?**  
Sets multiplied by reps multiplied by weight. I use it only as a simple comparison metric and document its limitations.

**How is a PR detected?**  
V1 defines a PR as the highest recorded weight for that exercise. The new weight must be greater than the previous maximum.

**How does Progress Watch work?**  
It looks at the last three recorded volume values. More than +2% is improving, less than -2% is a recent decrease, identical values mean no recent change, otherwise it is stable. Fewer than three records means not enough data.

**What happens with invalid input?**  
Reusable input functions keep asking until the user enters a positive valid number instead of allowing the application to crash.

**Why not use a database or web app?**  
The dataset and personal use case are small, and the assessment requires a command-line Python program. CSV/JSON keep the project suitable for the problem and easier to explain.

**How did AI help?**  
AI helped with planning, code generation/review, testing ideas and documentation. I record the assistance honestly, test the program, and I am responsible for understanding the submitted code.

**What are the sociotechnical considerations?**  
I separated personal records from files intended for Git, and I designed the output as transparent decision support instead of pretending the program provides medical or professional fitness advice.

**What are the main limitations?**  
The calculations depend on accurate manual input, training volume is simplified, Progress Watch uses only recent recorded volume, and the program does not make scientific or medical predictions.

## Final personal tasks before submission

- Re-run every important test on your Windows/VS Code setup.
- Replace or personalise the starter Exercise Vault/routines so they truly match what you do.
- Enter genuine data only if you are comfortable storing it locally.
- Verify `.gitignore` before pushing.
- Save the real AI conversations using the unit's required format.
- Build a sustained, truthful Git history from the work you actually do.
- Review the official cover page requirements.
- Export the required README/documentation PDF.
- Record the required video with your face visible.
- Practise the live demonstration and code explanation.
- Create the required Blackboard ZIP/PDF/MP4 submissions from the final version.
