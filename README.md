# cinematic shorts bot — real footage + readable fonts (2025 style)

**What it does**
- Pulls actual cinematic B‑roll from **Pexels** (free, commercial use)
- Overlays **readable kinetic captions** using **font presets** that match the vibe
- Adds a copyright‑safe **trap beat**
- Exports **1080×1920** MP4 (Shorts‑ready, <=60s)
- Auto‑uploads via GitHub Actions (optional)

## Font presets (set `FONT_PRESET` variable)
- `clean` – white bold with black stroke, translucent dark box (most readable)
- `gritty` – bold white with solid dark box (gym/city vibe)
- `romance` – warm cream serif + soft shadow (relationship quotes)
- `tech` – crisp mono‑style + translucent box (AI/facts vibes)

## Setup
1. Add these **Secrets** (Repo → Settings → Secrets and variables → Actions → New repository secret):
   - `PEXELS_API_KEY` (get free key at pexels.com → API)
   - `YOUTUBE_CLIENT_ID`
   - `YOUTUBE_CLIENT_SECRET`
   - `YOUTUBE_REFRESH_TOKEN`
2. Optional **Variables** (same page → Variables):
   - `NICHES` = `motivation,facts,list,relationship`
   - `FONT_PRESET` = `clean` (or `gritty|romance|tech`)
   - `SECONDS_PER_LINE` = `2.0`
   - `CTA` = `follow for more → @yourchannel`
   - `YOUTUBE_PRIVACY` = `public` or `unlisted`
   - `ADD_CTA` = `1` (set `0` to remove CTA line)
3. Run it: Actions → **auto-shorts** → Run workflow. Video is also saved as artifact.

**Policy**
- Pexels license allows free commercial use; no attribution required.
- Music is generated in code (no copyright).
- Keep text advertiser‑friendly for YPP.

