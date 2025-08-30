import os, sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload(file_path, title, description, tags=None, privacy="unlisted"):
    cid = os.getenv("YOUTUBE_CLIENT_ID")
    csec = os.getenv("YOUTUBE_CLIENT_SECRET")
    rtok = os.getenv("YOUTUBE_REFRESH_TOKEN")
    missing = [k for k,v in {"YOUTUBE_CLIENT_ID":cid,"YOUTUBE_CLIENT_SECRET":csec,"YOUTUBE_REFRESH_TOKEN":rtok}.items() if not v]
    if missing:
        print(f"[upload] missing: {', '.join(missing)} — skipping upload", file=sys.stderr)
        return {"status":"skipped","missing":missing}
    creds = Credentials(None, refresh_token=rtok, token_uri="https://oauth2.googleapis.com/token",
                        client_id=cid, client_secret=csec, scopes=SCOPES)
    creds.refresh(Request())
    yt = build("youtube","v3",credentials=creds)
    body = {
        "snippet": {"title": title[:100], "description": description[:5000], "tags": tags or ["shorts","viral"], "categoryId":"22"},
        "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False}
    }
    media = MediaFileUpload(file_path, mimetype="video/mp4", chunksize=-1, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
    return resp
