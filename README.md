# rioxbt/makefun-auto-news-image-20261118-entri

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/rioxbt/makefun-auto-news-image-20261118-entri/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/rioxbt/makefun-auto-news-image-20261118-entri/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image that sums up the world news of Wednesday 18 November 2026, entered in
[make.fun's "Sum up 18 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261118).

The picture is a dated front board: the day's date across the top, then eight
story cards, each naming a place and a field and giving the story in a headline
and one line of detail —

| Place | Story |
| --- | --- |
| Manila · Asia-Pacific | Quad leaders meet as the ASEAN summit closes |
| Shenzhen · Asia | Putin arrives for APEC as Trump heads in |
| Strait of Hormuz · Middle East | US and Iran trade fresh strikes |
| Kyiv · Europe | Ukraine strikes the Kerch Bridge again |
| Wall Street · Economy | Tech selloff deepens as Nvidia reels |
| Washington · Health | US loses measles elimination status |
| Antalya · Climate | COP31 concedes 1.5C will be overshot |
| Maputo · Africa | Opposition leader Mondlane goes on trial |

A footer lists four more of the day's stories (GTA VI, Brazil's budget vote,
Ghana's cocoa warning, Ecuador's suit against the US) so the picture is not one
region's or one beat's. Nothing is drawn from outside the repository: the file
is a 1024x1024 PNG, 132,386 bytes, well inside the gate's 1 MiB and 1024px caps.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) checks that `entry.png` beside it is
a PNG of a size the gate accepts, then copies it, byte for byte, to
`/output/entry.png`. It reads no network, no clock and no random source, so the
grader's two runs write the same bytes.

`tools/make_entry_image.py` renders `entry.png` from the story list above, so
the picture is reproducible rather than an opaque blob:

```sh
python3 tools/make_entry_image.py entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
