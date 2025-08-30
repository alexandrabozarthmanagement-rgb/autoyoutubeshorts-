import os
from datetime import datetime
from templates import pick_niche, build
from pexels_fetch import fetch_broll
from editor import assemble
from uploader import upload

def main():
    niche = os.getenv("NICHE_OVERRIDE","").strip().lower() or pick_niche()
    queries, lines, title, desc, tags = build(niche)

    # Fetch real cinematic footage from Pexels
    broll = fetch_broll(queries, per_query=2, per_page=18)

    preset = os.getenv("FONT_PRESET","clean")  # clean | gritty | romance | tech
    seconds = float(os.getenv("SECONDS_PER_LINE","2.0"))
    out_path = assemble(broll, lines, seconds_per_line=seconds, font_preset=preset, out="short.mp4")

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    title = os.getenv("SHORTS_TITLE", title).replace("{TIME}", now)
    desc = os.getenv("SHORTS_DESCRIPTION", desc)

    priv = os.getenv("YOUTUBE_PRIVACY","unlisted")
    result = upload(out_path, title, desc, tags=tags, privacy=priv)
    print(f"[done] niche={niche} preset={preset} result={result}")

if __name__ == "__main__":
    main()
