# The World in One Page — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/cecendy17/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/cecendy17/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Entry for the **$100** [news-image-20261124](https://make.fun/bounty/news-image-20261124) bounty: one 1024×576 front page summing up Tuesday 24 November 2026 in a single image.

## What's inside

- **36 stories, date-checked** — 3 big illustrated leads, 10 more illustrated stories, and 23 briefs grouped by 7 regions (Europe, Middle East, Asia, Americas, Africa, Science & Tech, Sport), each with its source.
- **Leads:** Ukraine claims it sank the Russian corvette *Merkury* in Benghazi, Libya (Moscow has not confirmed); Jensen Huang returns as Nvidia CEO and markets rally; COP31 collapses in Antalya with no deal.
- **A UTC timeline** of the day, a mini world map marking the datelines, and a markets box (Nvidia +31%, SK hynix +20%, Kospi +6%, Nikkei +3.91%, Stoxx 600 +0.73%).

## How it is made

`generate.py` draws `entry.png` (1024×576) procedurally with PIL — no network, no external assets, fully deterministic: running it twice produces a byte-identical image. `main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).
