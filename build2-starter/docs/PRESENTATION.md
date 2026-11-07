# What goes on the ten slides, and what does the panel ask?

Ten minutes, ten slides, then six minutes of questions on Saturday.

## Which rules apply to every slide?

- Slide 1 is the answer. The panel has read the brief, so no slide restates it; a slide that does scores zero for evidence discipline.
- Every number on a slide has a screenshot beside it showing the line of code and the output that produced it. Save them in `evidence/`.
- Each slide's title is the question it answers, and its owner's name is on it.
- A clue that changed a decision is named on the slide where the decision appears.
- Slide 7 runs `python src/nightly.py --from 2017-08-18 --nights 14` live from your frozen commit, reading the method saved in `models/`, so nothing retrains on stage.

## Which slides, owned by whom, with which evidence?

| Slide | Owner | Seconds | Title | Evidence that must appear |
|---|---|---|---|---|
| 1 | Client Lead | 45 | What should the revenue manager do tomorrow night? | The nightly table for the next fourteen nights, with one sentence above it |
| 2 | Client Lead | 45 | What is decided, and what do the two wrong calls cost? | The frame sentence and the metric tree, with the north star and the ceiling |
| 3 | Client Lead and Data Lead | 75 | What did the data say that the brief did not? | The check of the brief's numbers, your answer to observation 1 with the question you sent the client, and the travel-partner view of rate against volume |
| 4 | Data Lead | 60 | Which columns did the hotel know on the day of booking? | The three-bin audit, and the three AUCs from `docs/COLUMNS.md` |
| 5 | Model Lead | 75 | Which method wins, and under which measure? | The method table from `python src/backtest.py` on the proof period |
| 6 | Model Lead | 45 | What would flip the choice? | Buffer against walks on the choose period, and one changed condition |
| 7 | Build Lead | 90 | Does it run? | A live run of the MVP command, and the architecture diagram |
| 8 | Build Lead | 60 | Which three grilling questions changed our plan? | Three rows from the grill logs: question, answer, change |
| 9 | Data Lead | 60 | What did the AI build get wrong, and what did it expose in ours? | The comparison table and one screenshot of the branch |
| 10 | Client Lead | 45 | What is the honest range, and what comes next? | The full-night caveat by hotel, and the three-week roadmap |

The seconds add up to 600.

## Which questions should we expect?

The panel picks who answers, never the team.

- Why the night and not the booking?
- Which column would you drop if you learned it is set at check-in, and how much AUC would you lose?
- Which of your methods won on AUC, which won on money, and why are they not the same one?
- What happens in January, when the resort is not full?
- Which number in the brief was wrong, and how did you find it?
- Show me the line that sets the buffer.
- If walking a guest cost EUR 1,000, what would change?
- What did the AI build do that you would never ship?
- How many walks per 1,000 did your rule produce on the proof period?
