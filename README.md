# The World in One Day — Friday 27 November 2026

A one-page newspaper poster summing up the world news of Friday
27 November 2026, drawn entirely in code.

## The image

`main.py` (Python 3.13, standard library only) draws a 1024x1024 PNG
and writes it to `/output/entry.png`. It uses no network and no
external assets: every pixel comes from the program itself — a small
built-in 5x7 bitmap font, rectangles, circles, lines and triangles —
so two runs produce byte-identical output.

The poster names the day prominently — **27 NOVEMBER 2026** — and
covers six of the day's most consequential stories, across regions
and fields:

1. **Middle East** — Iranian strikes hit Kuwait: a drone attack on a
   steel plant kills two Italians; Iran denies it, and a Saudi
   refinery is hit too.
2. **Europe** — EU leaders meet in Brussels over a 1.7 trillion euro
   budget and aid for Ukraine; Trump tells Putin to pull back his
   aggression.
3. **Gaza** — Israeli strikes kill Palestinians in Gaza City,
   including a deputy education minister; Hamas weighs its response.
4. **America** — A Thanksgiving storm postpones the 100th Macy's
   Thanksgiving Day Parade, a first, and leaves 500,000 homes
   without power.
5. **Asia** — Kim Jong Un vows a bigger nuclear arsenal and rejects
   Trump's offer of talks.
6. **Sport** — Lille stun Bayern Munich, handing them their first
   defeat of the season.

A footer ticker adds the rest of the day: Black Friday sales, UK net
migration at its lowest since 1997, a new ECB chief, Serbia's
presidential vote set for 27 December, and a fuel-truck fire in
Egypt that killed more than 30 people.

All events were reported on 27 November 2026.

## Running it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## Files

- `main.py` — the program (the whole entry)
- `README.md` — this file
- `LICENSE` — MIT
- `.makefun/owner.json` — payout wallet claim
