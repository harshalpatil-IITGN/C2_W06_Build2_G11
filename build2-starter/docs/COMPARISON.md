# What did the AI build get wrong, and what did it expose in ours?

**Owner:** Data Lead. **Challenger:** Build Lead. **When:** started on Thursday, finished on Friday.

Compare your build on `main` with the AI build on the `ai-benchmark` branch, row by row. Every cell points to a file and a line, or to a log excerpt. "Same" is an acceptable verdict when it is true.

| Row | Our build | AI build | Verdict |
|---|---|---|---|
| What counts as a cancellation, and which bookings are scored | | | |
| Unit of decision (night or booking) | | | |
| Columns used, and the bin each sits in | | | |
| Split (time or random), and where the buffer was chosen | | | |
| Baselines run before any model | | | |
| Walk ceiling respected on the choose period and reported on proof | | | |
| Euros, rooms and walks per 1,000 on the proof period | | | |
| Runs end to end with one command | | | |
| Lines of code a team member can explain | | | |

## Which gaps in our build did the AI build expose?

_Up to three, each naming a file and line in our build, or an excerpt from a log. If you found none, say so and name the file that shows it._

<!-- answer:4 -->

## Which mistakes did the AI build make that ours did not?

_Up to three, each naming a file and line on the `ai-benchmark` branch. If you found none, say so and name the file that shows it._

<!-- answer:4 -->

## What would we take from the AI build, and what would we never ship?

_Two sentences, each pointing to a file and line._

<!-- answer:2 -->
