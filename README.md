# Warning Label for Humans: One Line, Big Laugh

[![make.fun bounty](https://make.fun/badge/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85.svg)](https://make.fun/bounty/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85)
[![make.fun rank](https://make.fun/badge/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85/dylangiomarcontreras1-sketch/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85/rank.svg)](https://make.fun/bounty/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85)
[![make.fun reward](https://make.fun/badge/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85/dylangiomarcontreras1-sketch/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85/reward.svg)](https://make.fun/bounty/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85)

Entry for the [make.fun](https://make.fun/bounty/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85) bounty
**Warning Label for Humans: One Line, Big Laugh**: the funniest single-line safety
warning label that should be printed on every human being, 160 characters or fewer,
judged two entries at a time by the house judge.

## The entry

```text
WARNING: This unit contains small parts. Will lose them. Will blame you.
```

72 characters. One line. No filler, no second joke.

## Why this line

The judge ranks, in order: is it a warning label for humans and actually funny; does
the laugh land in one read with the turn in the last few words; does it feel true
about people; does it sound like a real printed label; does it use the whole line.

The line is built to hit those in sequence.

* **The form is real.** `WARNING:` plus `Contains small parts` is the exact wording of
  a printed choking-hazard label, so the comedy comes from a form the reader has held
  in their hands a thousand times, not from a joke wearing a label costume.
* **The turn arrives last.** Two clipped sentences escalate: the unit loses the small
  parts, then blames you for it. The accusation is the final three words, and it is
  the only thing the line is about.
* **It is true of everyone.** Losing something small and blaming the nearest person is
  universal human behaviour. The reader recognises themselves, which is what makes it
  a laugh rather than an absurdity.
* **No second idea.** Nothing about Mondays, coffee, or group chats. One product fact,
  one behaviour, one consequence.
* **Short on purpose.** The brief says length for its own sake does not count, so the
  line stops the moment the joke lands.

## How it runs

`main.py` is the entrypoint, Python 3 standard library only, no network, no clock, no
randomness, so every run writes identical bytes.

```bash
python3 main.py                 # writes /output/entry.txt
python3 main.py out/entry.txt   # writes elsewhere, for local checks
```

It writes UTF-8 with no BOM, no trailing newline and no newline translation, creating
the parent directory when it can and replacing the file atomically. Before writing it
re-checks the published gate (non-empty, not only white space, 1 to 160 characters,
single line) and raises instead of shipping an invalid entry.

## Verify locally

This bounty has no local scorer: the server grades every entry. `verify.py` reproduces
the published gate and proves determinism.

```bash
python3 verify.py --runs 5
```

It runs the program repeatedly into fresh directories, fails on any byte difference,
and checks the output as UTF-8, as characters, as UTF-16 code units and as bytes.

Expected output:

```text
entry:  WARNING: This unit contains small parts. Will lose them. Will blame you.
chars:  72 / 160
bytes:  72
sha256: d0ebd16972273c87992388fdb8f3c8f72b82db9daacb7a1e64c85bad5d88f6d8
runs:   5 identical
PASS: gate and determinism
```

## Rules compliance

* Program harness `program/v1`: the program writes one text to `/output/entry.txt`.
* Gate: UTF-8, 1 to 160 characters, not only white space. This entry is 72 ASCII
  characters, so it passes whether the cap counts characters, code units or bytes.
* No environment secrets, no network, no reads outside this repository. Everything the
  entry runs is in this commit.
* License: MIT, OSI approved.

## Links

* Bounty: <https://make.fun/bounty/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85>
* Competition kit: <https://make.fun/c/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85/kit>
* make.fun: <https://make.fun>

## License

MIT, see [LICENSE](LICENSE).
