# Where does the AI benchmark live?

On the `ai-benchmark` branch, never on `main`. The steps and both prompts are in `docs/AI_WORKFLOW.md`. On the branch this folder holds three things:

- `PLAN_AI.md`, the AI's plan, saved before you approve it;
- `run.py`, the AI's code, edited only to fix an environment error;
- the output of `python ai_benchmark/run.py`, pasted into `RESULT.md`.

The chat itself goes to `ai_logs/` on `main`, and `docs/COMPARISON.md` sets the two builds side by side.
