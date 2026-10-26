# Milecast walkthrough — natural voiceover script

Video (interactive cursor recording, ~3.5 min picture / stretches longer with your pauses):

`walkthrough/Milecast-Interactive-Walkthrough.mp4`

Speak loose. Leave space. Don’t rush. The recording already has slow/fast cursor moves, pointing, slider drag, and clicks — match those moments. If you need 5–10 minutes total, just… sit on the pauses. Talk slower. Repeat a thought. That’s literally the point.

---

## How to record your voice on top

1. Import the MP4 into CapCut / Descript / Premiere / Loom  
2. Mute nothing (video is silent)  
3. Read below like you’re explaining to a friend on a call  
4. If you mess a line, pause and say it again — that’s fine  

Markers mean:
- `[...]` = short breath / think pause (~1–2 sec)
- `[long]` = let the cursor finish moving (~3–5 sec)
- `(pointing)` = you’re talking while cursor is circling that thing

---

## Full script (casual English)

### 0:00 — open / brand
Okay so… yeah.  
[...]  
This is Milecast.  
[...]  
Uh, weather-aware truck routing. Spotter assessment thing.  
[long]  
React on the front, Django on the back… live providers, not mocked stuff.

### Home / why it exists
So the idea is pretty simple.  
[...]  
Driver puts where they’re going… when they leave… how heavy the load is…  
[long]  
and then we try to pick the safer corridor, not just the fastest one.  
[...]  
Yeah.

### Trip inputs `(pointing at form)`
Alright, inputs.  
[...]  
Origin… I’m leaving Denver.  
[long]  
Destination… Kansas City.  
[...]  
Departure time… like, later tonight.  
[...]  
Load weight… twenty-eight thousand pounds.  
[long]  
Checkpoint spacing… I’m putting every fifty miles so it’s not too noisy.  
[...]  
You can do ten or twenty-five also, same idea.

### Risk rules panel `(pointing)`
And over here… these are the PDF rules.  
[long]  
Wind, rain, snow… thresholds.  
[...]  
And if the load is heavy, wind gets stricter.  
[...]  
Like forty-five to fifty-four wind plus over thirty thousand… that’s no travel.  
[long]  
Yeah, that part matters.

### Forecast slider `(cursor on slider — drag it)`
This slider… this is the zero to forty-eight hour thing.  
[...]  
So weather is checked at the truck ETA…  
[long]  
plus whatever offset you put here.  
[...]  
I’m gonna drag it a bit…  
[long]  
…and later after we build the plan, moving this refreshes the corridor.  
[...]  
Live. Not fake.

### Build plan `(click the orange button)`
Okay… build weather-aware plan.  
[long]  
Give it a second… it’s hitting real geocoding, routing, Open-Meteo…  
[...]  
Should come back with three routes.

### Results / three corridors `(hover cards)`
Alright. Three corridors.  
[...]  
Prairie… Ridge… River.  
[long]  
You get time, miles, checkpoints…  
[...]  
severe miles, high miles, no-travel, average risk.  
[long]  
Recommended one is highlighted.  
[...]  
Don’t just look at distance — look at the risk numbers.

### Map heatmap `(move slowly along the green corridor)`
Map side…  
[...]  
These dots are checkpoints.  
[long]  
Color is the risk. Green is low… then it goes up if weather gets nasty.  
[...]  
I’m just kinda tracing the corridor here…  
[long]  
so you can see it’s not one color for the whole trip. It’s sampled along the way.

### Open checkpoint details `(click details)`
If I open checkpoint details…  
[long]  
you get ETA per stop… and the risk badge.  
[...]  
That’s the “weather at arrival time” part from the brief.

### Recommendation logic `(point at recommended card)`
Ranking is…  
[...]  
fewest severe first…  
[...]  
then high…  
[...]  
then average risk…  
[...]  
then travel time.  
[long]  
No-travel is worse than severe, so that goes first basically.  
[...]  
So yeah — Ridge won here even if another one is a bit shorter. Safer wins.

### Stack / wrap
Backend Django REST… frontend Next…  
[...]  
Nominatim, OSRM… Open-Meteo for weather.  
[long]  
Didn’t build a routing engine. Just used providers like the PDF allows.  
[...]  
That’s the whole flow.  
[long]  
Thanks for watching — repo and demo links are in the notes.

---

## Presenter gesture cues (already in the video)

| Moment | Cursor behavior you should match when speaking |
|--------|--------------------------------------------------|
| Brand / headline | Slow drift, small circle |
| Form fields | Hover each field, occasional click-focus |
| Risk rules | Point down the list, not too fast |
| Slider | Grab and drag left→right (explain while dragging) |
| Build button | Pause on button, then click |
| Waiting | Idle micro-moves near button |
| Route cards | Hover recommended, then alternatives |
| Map | Slow trace along corridor, then faster hop to a checkpoint |
| Details | Click open / glance list |
| End | Drift to footer providers text |

## Tip
If your Loom needs 5–10 minutes: after “Thanks for watching”, keep talking for a minute — open one more checkpoint, nudge the slider again, compare Prairie vs Ridge out loud. The interactive recording already supports that pacing.
