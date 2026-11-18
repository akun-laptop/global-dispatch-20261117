# THE GLOBAL DISPATCH — 17 November 2026

Entry for make.fun **news-image-20261117**: "Sum up 17 November's
world news in one image."

A broadsheet-style front page drawn entirely with PIL
(`draw.py`, no AI imagery): a full-width lead on the Kerch Bridge,
a "BY THE NUMBERS" strip, and six story cards with small
vector-style illustrations. `main.py` (stdlib only) copies the
rendered `entry.png` to the output directory.

## The seven stories

Every story was verified live as first reported on **17 November
2026 (UTC)** before drawing:

1. **Kerch Bridge span falls** (lead) — Ukraine's overnight
   missile-and-drone strike collapses the road arch into the
   Kerch Strait; Zelensky calls it an "unprecedented" operation.
   First report 17 Nov UTC: TheBullPost 13:25 UTC; AP via MTPR
   updated 17 Nov 13:24 MST.
2. **Quad summit, Manila** — Trump, Modi, Albanese and Takaichi
   meet, the first Quad leaders' summit in over two years; joint
   maritime patrols, cable protection, a 2027 business forum.
   First report 17 Nov UTC: JKN 14:25 UTC.
3. **Iran drones target US radar in Bahrain** — third Iranian
   strike on US targets there in five days; Bahrain says the
   drones were intercepted, no US casualties.
   First report 17 Nov UTC: Bozok Media 07:35 UTC; AP datelined
   Nov 17.
4. **Japan scrambles jets** — two suspected Russian aircraft enter
   Japanese airspace near Fukuoka for about three minutes each;
   Tokyo lodges a "very stern protest".
   First report 17 Nov UTC: Reuters 04:33 UTC.
5. **Britain sanctions eight settlement firms** — asset freezes
   on Israeli construction companies and on Tzav 9, the group
   accused of blocking Gaza aid convoys.
   First report 17 Nov UTC: GOV.UK announcement; JBizNews 12:14 UTC.
6. **An-12 crash in Siberia, 19 killed** — Russian military
   transport goes down near Yagunovo, Kemerovo region; technical
   fault suspected.
   First report 17 Nov UTC: Reuters 19:15 UTC.
7. **US loses measles-free status after 26 years** — PAHO
   declares endemic transmission is back (5,412 cases in 2026);
   Mexico and Bolivia lose the status too.
   First report 17 Nov UTC: Reuters 16:18 UTC; PAHO announcement
   17 Nov.

## Stories checked and dropped

- **Gérard Depardieu drops appeal** — his statement was issued
  on Monday 16 Nov (Paris time); first reports 16 Nov UTC. Wrong
  day for this contest.
- **JPMorgan Chase software bug / Zelle delays** — the outage
  happened Monday 16 Nov and was first reported that day
  (Reuters, Chase statement). Wrong day for this contest.

Verified alternate not used (8th story): Mongolia's President
Khurelsukh announces resignation over corruption allegations —
announced 17 Nov UTC (AP 12:42 UTC).

## Reproduce

    python3 draw.py        # regenerates entry.png (deterministic)
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Output: 1024x1024 PNG, well under the 1 MiB limit.
