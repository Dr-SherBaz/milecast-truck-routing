# Milecast walkthrough — voiceover script

Video file (silent, ready for your narration):

`walkthrough/Milecast-Walkthrough-VOICEOVER-READY.mp4` (~4 min 31 sec)

## How to add your voice

1. Open CapCut, Descript, Premiere, or Loom
2. Import the MP4
3. Record narration using the script below (pause/extend scenes if you want a full 5–10 min Loom)
4. Export and submit the link

## Timed script

| Time | On screen | Say this |
|------|-----------|----------|
| 0:00–0:12 | Title | “Hi — I’m presenting Milecast, my weather-aware truck routing app for the Spotter full-stack assessment.” |
| 0:12–0:26 | Requirements | “The brief asks for React plus Django: origin, destination, departure time, load weight; three route options; weather every 10, 25, or 50 miles at ETA; PDF risk rules; a recommendation; and a map heatmap with a 0–48 hour forecast slider.” |
| 0:26–0:48 | Home UI | “Here’s the Milecast UI. Branding and copy explain the safety-first decision flow. Stack badge shows React and Django with live providers.” |
| 0:48–1:00 | Inputs card | “The trip form captures everything the PDF requires.” |
| 1:00–1:22 | Filled inputs | “I’m planning Denver to Kansas City, departure this evening, 28,000 pound load, checkpoints every 50 miles. The forecast slider starts at zero hours.” |
| 1:22–1:34 | Plan title | “Building the plan calls the Django API, which geocodes with Nominatim, routes with OSRM, and pulls Open-Meteo weather at each checkpoint ETA.” |
| 1:34–1:56 | Results | “We get exactly three corridors — Prairie, Ridge, and River — with travel time, distance, and risk summaries.” |
| 1:56–2:10 | Map title | “The map is the corridor weather heatmap.” |
| 2:10–2:32 | Map view | “Each checkpoint is colored by risk. Green means low. The recommended corridor is emphasized.” |
| 2:32–2:46 | Slider title | “The 0–48 hour forecast slider re-queries weather so the heatmap updates live for a later departure window.” |
| 2:46–3:08 | Results again | “You can compare severe miles, high miles, no-travel miles, and average risk on each card, and expand checkpoint ETAs.” |
| 3:08–3:24 | Ranking title | “Recommendation follows the PDF order: fewest severe miles, then high miles, then lowest average risk, then shortest travel time. No-travel outranks severe.” |
| 3:24–3:46 | Recommendation | “Here Ridge corridor wins with the cleanest average risk, even when another corridor is slightly shorter.” |
| 3:46–4:00 | Stack | “Backend is Django REST Framework. Frontend is Next.js. Providers: Nominatim, OSRM or optional OpenRouteService, and Open-Meteo. No custom routing engine.” |
| 4:00–4:12 | End card | “Thanks for watching — repo and hosted demo links are in the submission notes.” |

## Optional stretch to 5–10 minutes

After each UI scene, pause 10–20 seconds and walk through a click live in Loom (slider move, open checkpoint details, switch corridors). Keep this silent MP4 as the B-roll/title backbone.
