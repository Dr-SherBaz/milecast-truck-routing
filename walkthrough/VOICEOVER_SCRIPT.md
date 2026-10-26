# Milecast walkthrough — timed voiceover script

**Video:** `walkthrough/Milecast-Interactive-Walkthrough.mp4` (~3:20)  
**Cue source:** `walkthrough/timeline.json` (logged live during this exact recording)

Speak loose. Don’t chase perfect grammar. Start each block when the slot starts — the cursor is already doing the thing listed under **Cursor**.

Markers:
- `[...]` = short breath (~1 sec)
- `[long]` = let the cursor finish (~2–3 sec)
- Stay inside the slot; if you finish early, just breathe until the next cue

---

## Exact timing slots (match cursor)

### `0:00–0:02` · start
**Cursor:** idle / appears on page  

Okay so… yeah.  
[...]

### `0:02–0:05` · brand_move
**Cursor:** slow move → Milecast logo  

This is… uh… Milecast.

### `0:05–0:09` · brand_label
**Cursor:** circle around logo *(label: “Milecast”)*  

Weather-aware truck routing. Spotter assessment thing.  
[long]

### `0:09–0:16` · headline
**Cursor:** move + wobble on headline *(label: “what this app does”)*  

So the idea is pretty simple.  
[...]  
Driver puts where they’re going… when they leave… how heavy the load is…  
[long]  
and we try to pick the safer corridor, not just the fastest one.

### `0:16–0:22` · stack_badge
**Cursor:** circle top-right stack badge *(label: “React + Django”)*  

React on the front, Django on the back…  
[...]  
live providers. Not mocked stuff.

### `0:22–0:28` · origin
**Cursor:** click Origin → type Denver *(label: “origin”)*  

Alright, inputs.  
[...]  
Origin… I’m leaving Denver.

### `0:28–0:34` · destination
**Cursor:** click Destination → type Kansas City *(label: “destination”)*  

Destination… Kansas City.  
[...]  
Yeah.

### `0:34–0:39` · weight
**Cursor:** click Load weight → type 28000 *(label: “load weight”)*  

Load weight… twenty-eight thousand pounds.  
[long]

### `0:39–0:44` · spacing
**Cursor:** open spacing select → every 50 miles *(label: “every 50 miles”)*  

Checkpoint spacing… every fifty miles so it’s not too noisy.  
[...]  
Ten or twenty-five works too, same idea.

### `0:44–0:56` · risk_rules
**Cursor:** slow wander down PDF risk rules panel *(label: “PDF risk rules”)*  

And over here… these are the PDF rules.  
[long]  
Wind, rain, snow… thresholds.  
[...]  
Just pointing through them…

### `0:56–1:01` · load_wind
**Cursor:** circle heavy-load / wind line *(label: “heavy load + wind”)*  

If the load is heavy, wind gets stricter.  
[...]  
Like forty-five to fifty-four wind plus over thirty thousand… that’s no travel.  
[long]  
Yeah, that part matters.

### `1:01–1:06` · slider_arrive
**Cursor:** move onto forecast slider *(label: “0–48h forecast slider”)*  

This slider… zero to forty-eight hours.  
[...]  
Weather is checked at the truck ETA… plus whatever offset you put here.

### `1:06–1:09` · slider_drag
**Cursor:** mouse down + uneven left→right drag  

I’m gonna drag it a bit…  
[long]

### `1:09–1:14` · slider_explain
**Cursor:** rest on slider *(label: “drag to shift forecast window”)*  

…and later after we build the plan, moving this refreshes the corridor.  
[...]  
Live. Not fake.

### `1:14–1:16` · slider_reset
**Cursor:** drag slider back toward 0h  

Okay I’m putting it back near zero for a clean plan…

### `1:16–1:22` · build_hover
**Cursor:** approach + wobble on orange CTA *(label: “build the plan…”)*  

Okay… build weather-aware plan.  
[long]

### `1:22–1:30` · build_click
**Cursor:** click Build → idle micro-moves while waiting  

Give it a second…  
[...]  
It’s hitting real geocoding, routing, Open-Meteo…  
[long]

### `1:30–1:32` · plan_api
**Cursor:** still waiting near button (API 200)  

…should be coming back now.

### `1:32–1:38` · results
**Cursor:** results heading in view *(label: “three corridors back”)*  

Alright. Three corridors.  
[...]  
Prairie… Ridge… River.

### `1:38–1:53` · map
**Cursor:** slow trace along green corridor *(label: “corridor heatmap”)*  

Map side…  
[...]  
These dots are checkpoints.  
[long]  
I’m just kinda tracing the corridor here…  
[...]  
so you can see it’s sampled along the way, not one color for the whole trip.

### `1:53–2:01` · map_hops
**Cursor:** faster hops on checkpoint dots *(label: “checkpoint colors = risk”)*  

Color is the risk. Green is low… gets nastier if weather gets bad.  
[long]

### `2:01–2:07` · card_0
**Cursor:** hover first alternative card *(label: “alternative”)*  

Prairie… that’s an alternative.  
[...]  
Time, miles, risk numbers…

### `2:07–2:15` · card_1
**Cursor:** circle recommended → click *(label: “recommended”)*  

And this one… recommended. Ridge.  
[long]  
Don’t just look at distance — look at the risk.

### `2:15–2:21` · card_2
**Cursor:** hover third alternative *(label: “another option”)*  

River is the other option… longer usually.

### `2:21–2:31` · checkpoints
**Cursor:** click checkpoint details → scan list *(label: “checkpoint ETAs”)*  

If I open checkpoint details…  
[long]  
you get ETA per stop… and the risk badge.  
[...]  
That’s the weather-at-arrival-time part from the brief.

### `2:31–2:39` · ranking
**Cursor:** circle recommended card *(label: “severe → high → avg risk → time”)*  

Ranking is…  
[...]  
fewest severe first… then high… then average risk… then travel time.  
[long]  
No-travel is worse than severe, so that goes first basically.  
[...]  
Ridge won even if another one’s a bit shorter. Safer wins.

### `2:39–2:51` · slider_live
**Cursor:** second slider drag after plan *(label: “nudge forecast… refreshes live”)*  

And this is the live part…  
[...]  
I nudge the forecast again…  
[long]  
corridor should refresh.

### `2:51–3:00` · refresh_wait
**Cursor:** idle after release *(label: “waiting on live refresh…”)*  

Just waiting on it…  
[long]  
yeah.

### `3:00–3:05` · compare
**Cursor:** hover Prairie then Ridge again  

Quick compare after refresh… Prairie… then Ridge.  
[...]

### `3:05–3:14` · providers
**Cursor:** point at footer providers *(label: “Nominatim · OSRM · Open-Meteo”)*  

Backend Django REST… frontend Next…  
[...]  
Nominatim, OSRM… Open-Meteo for weather.  
[long]  
Didn’t build a routing engine. Just used providers like the PDF allows.

### `3:14–3:20` · end
**Cursor:** drift center *(label: “thanks for watching”)*  

That’s the whole flow.  
[...]  
Thanks for watching — repo and demo links are in the notes.

---

## Quick cue sheet (teleprompter)

| Slot | Say the beat | Cursor is… |
|------|----------------|------------|
| 0:00–0:02 | “Okay so…” | idle |
| 0:02–0:09 | Milecast intro | logo circle |
| 0:09–0:16 | safer corridor idea | headline |
| 0:16–0:22 | React + Django | badge |
| 0:22–0:44 | fill origin → dest → weight → 50 mi | form typing |
| 0:44–1:01 | PDF risk + heavy load | rules panel |
| 1:01–1:16 | slider explain + drag + reset | forecast slider |
| 1:16–1:32 | build + wait | orange button |
| 1:32–2:01 | three routes + map trace | results / map |
| 2:01–2:21 | hover cards / recommended | route cards |
| 2:21–2:39 | checkpoints + ranking | details / recommended |
| 2:39–3:05 | live slider + compare | slider + cards |
| 3:05–3:20 | stack + thanks | footer / center |

---

## Tip
Need 5–10 min Loom? After `3:14`, keep talking over a freeze/loop of the last seconds, or record a second take opening one more checkpoint. The slots above are locked to **this** MP4.
