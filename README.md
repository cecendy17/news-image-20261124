# The World Today — 24 November 2026 in one image

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/cecendy17/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/cecendy17/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A broadsheet front page that sums up 24 November 2026's world news in a single
1024×576 image: **36 stories, date-checked**, across 7 regions.

- **Lead:** Ukraine claims it sank the Russian corvette *Merkury* off Benghazi, Libya
- **Lead:** Jensen Huang returns as Nvidia CEO; shares jump 31%
- **Lead:** COP31 in Antalya collapses with no deal after ~50 hours of overtime
- Plus 10 stories in pictures and 23 briefs by region, a UTC timeline of the day,
  and a mini world map showing where the news happened.

Bounty: https://make.fun/bounty/news-image-20261124

## How it was made

`generate.py` draws `entry.png` from scratch with Python + PIL only — no network,
no external images, fully deterministic. `main.py` copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`.

## Reproduce

```sh
python3 generate.py
python3 main.py
```
