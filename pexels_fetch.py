import os, requests, random

API = "https://api.pexels.com/videos/search"

def fetch_broll(queries, out_dir="broll", per_query=2, per_page=20):
    os.makedirs(out_dir, exist_ok=True)
    key = os.getenv("PEXELS_API_KEY")
    if not key:
        raise RuntimeError("Missing PEXELS_API_KEY")
    headers = {"Authorization": key}
    saved = []
    for q in queries:
        r = requests.get(API, headers=headers, params={"query": q, "per_page": per_page}, timeout=30)
        r.raise_for_status()
        data = r.json().get("videos", [])
        if not data:
            continue
        picks = random.sample(data, min(per_query, len(data)))
        for idx, v in enumerate(picks):
            files = [f for f in v.get("video_files", []) if f.get("file_type") == "video/mp4"]
            # Prefer vertical-ish, then by width (smaller first to save time)
            files.sort(key=lambda f: (abs((f.get("width",1280)/max(1,f.get("height",720))) - (9/16.0)), f.get("width",99999)))
            if not files:
                continue
            url = files[0]["link"]
            vr = requests.get(url, timeout=60)
            vr.raise_for_status()
            path = os.path.join(out_dir, f"{q.replace(' ','_')}_{idx}.mp4")
            with open(path, "wb") as f:
                f.write(vr.content)
            saved.append(path)
    # Shuffle to vary sequence
    random.shuffle(saved)
    # Cap total to 4 scenes for pacing
    return saved[:4]
