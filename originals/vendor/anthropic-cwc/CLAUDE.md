<!-- Copyright 2026 Anthropic PBC -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Long-running conventions for this project

## Always start here
Before doing anything else, read `PROGRESS.md`. It is your handoff note from the previous session. If it doesn't exist yet, create it now with four sections (`## Done`, `## In progress`, `## Next`, `## Notes`) and leave them empty. Then run `git log --oneline -10` to see what was just committed, and run the project's smoke test (or `npm run build` / `npm test`) once so you know you're starting from a working tree, not a broken handoff.

## One feature at a time
Work on exactly one item from `PROGRESS.md` per session. Finish it (tests passing, screenshot verified) before starting another. If the user gives you a new task mid-session, add it to `PROGRESS.md` and finish the current item first.

## Proof before passing
A test is only "passing" after you have:
1. Run it against the live app (Playwright screenshot or equivalent)
2. Opened the resulting screenshot or console log with the Read tool
3. Confirmed it shows what it should

The `verify-gate` hook will deny writes to `test-results.json` until you have opened evidence. Do not try to work around it.

## Keep `PROGRESS.md` current
After each completed item, update `PROGRESS.md`: check off what's done, add what you learned, note what's next. Future sessions read this file cold.

## Commit often
The `Stop` hook commits tracked changes at session end, but also `git add` new files and commit yourself at meaningful checkpoints with descriptive messages.

## If you're told to stop
`OPERATOR STEERING:` messages come from a human via the steer hook. Treat them as higher priority than your current plan.
