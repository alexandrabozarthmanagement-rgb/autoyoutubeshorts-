import os, math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, VideoClip, AudioClip

W, H = 1080, 1920
FPS = 30

SAFE_MARGIN = 80  # keep captions above/below UI zones

def _font_paths():
    # Use fonts commonly available on GitHub runners; fallback to default.
    return [
        "DejaVuSans-Bold.ttf",        # clean, bold
        "DejaVuSerif-Bold.ttf",       # romance/serif vibe
        "DejaVuSansMono.ttf"          # tech/mono
    ]

def _pick_font(preset: str, size: int):
    paths = _font_paths()
    path = paths[0]
    if preset == "romance":
        path = paths[1] if os.path.exists(paths[1]) else paths[0]
    elif preset == "tech":
        path = paths[2] if os.path.exists(paths[2]) else paths[0]
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def _caption_style(preset: str):
    # returns fill color and box alpha
    if preset == "gritty":   # bold white with black box
        return (255,255,255), (0,0,0,160)
    if preset == "romance":  # warm cream with soft shadow
        return (250,240,230), (0,0,0,120)
    if preset == "tech":     # neon-ish white with translucent dark
        return (240,255,255), (0,0,0,140)
    # default clean
    return (255,255,255), (0,0,0,150)

def _wrap(draw, text, font, max_w):
    words, lines, line = text.split(), [], ""
    for w in words:
        test = (line + " " + w).strip()
        bbox = draw.textbbox((0,0), test, font=font, stroke_width=0)
        if bbox[2]-bbox[0] <= max_w:
            line = test
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

def load_and_crop(path, zoom_speed=0.025, duration_limit=2.4):
    clip = VideoFileClip(path).without_audio()
    w,h = clip.size
    ar_target = 9/16
    ar = w/h
    if ar > ar_target:
        new_w = int(h*ar_target)
        x1 = (w-new_w)//2
        clip = clip.crop(x1=x1, y1=0, x2=x1+new_w, y2=h)
    else:
        new_h = int(w/ar_target)
        y1 = (h-new_h)//2
        clip = clip.crop(x1=0, y1=y1, x2=w, y2=y1+new_h)
    clip = clip.resize((W,H))
    # cinematic zoom
    def fl_time(get_frame, t):
        z = 1 + zoom_speed*t
        frame = get_frame(t)
        img = Image.fromarray(frame)
        cw,ch = int(W/z), int(H/z)
        x = (W-cw)//2; y = (H-ch)//2
        img2 = img.crop((x,y,x+cw,y+ch)).resize((W,H), Image.LANCZOS)
        # mild vignette
        mask = Image.new("L", (W,H), 0)
        d = ImageDraw.Draw(mask)
        d.ellipse([-W*0.2, -H*0.2, W*1.2, H*1.2], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(120))
        img2 = Image.composite(img2, Image.new("RGB",(W,H),(10,10,10)), mask)
        return np.array(img2)
    clip = clip.fl(fl_time, apply_to=['mask'])
    if clip.duration > duration_limit:
        clip = clip.subclip(0, duration_limit)
    return clip

def captions_overlay(lines, seconds_per_line=2.0, font_preset="clean", box=True):
    total = max(6.0, len(lines)*seconds_per_line + 0.6)
    fill, box_rgba = _caption_style(font_preset)
    font = _pick_font(font_preset, 90)

    def make_frame(t):
        img = Image.new("RGBA",(W,H),(0,0,0,0))
        d = ImageDraw.Draw(img)
        idx = min(int(t // seconds_per_line), len(lines)-1)
        text = lines[idx]
        # wrap in safe width
        max_w = int(W*0.88)
        wrapped = _wrap(d, text, font, max_w)
        # measure block
        line_hs = []
        total_h = 0
        for ln in wrapped:
            bbox = d.textbbox((0,0), ln, font=font, stroke_width=6)
            h = bbox[3]-bbox[1]
            line_hs.append((ln, bbox, h))
            total_h += h + 12
        y = int(H*0.68) - total_h//2
        y = max(SAFE_MARGIN, min(H - SAFE_MARGIN - total_h, y))
        # draw background box
        if box:
            pad = 26
            top = y - 18
            box_w = max(b[1][2]-b[1][0] for b in line_hs)
            left = (W - box_w)//2 - pad
            right = (W + box_w)//2 + pad
            bottom = y + total_h + 18
            ImageDraw.Draw(img, 'RGBA').rectangle([left, top, right, bottom], fill=box_rgba)
        # draw text with stroke
        y2 = y
        for ln, bbox, h in line_hs:
            tw = bbox[2]-bbox[0]
            x = (W - tw)//2
            d.text((x, y2), ln, font=font, fill=fill, stroke_width=8, stroke_fill=(0,0,0,255))
            y2 += h + 12
        # progress bar
        prog = min(max(t/total,0),1)
        bar_w = int(W*prog)
        d.rectangle([0,H-24,bar_w,H-14], fill=(255,255,0,255))
        return np.array(img)

    return VideoClip(make_frame=make_frame, duration=total).set_fps(FPS)

def trap_audio(duration, bpm=122):
    sr = 44100
    beat = 60.0/bpm
    two_pi = 2*math.pi
    def audio_fn(tt):
        t = np.array(tt, dtype=float)
        kick = 0.58*np.sin(two_pi*60*t)*(np.maximum(0, 1-((t%beat)/0.22)))
        hats = 0.10*np.sign(np.sin(two_pi*8000*t))*(np.sin(two_pi*(1/(beat/2))*t)>0)
        bass = 0.30*np.sin(two_pi*110*t)
        side = 0.55 + 0.45*(1-((t%beat)/beat))
        mix = (kick + hats + bass*0.7) * side
        return np.vstack([mix,mix]).T
    return AudioClip(make_frame=audio_fn, duration=duration, fps=sr)

def assemble(broll_paths, lines, seconds_per_line=2.0, font_preset="clean", out="short.mp4"):
    scenes = [load_and_crop(p) for p in broll_paths]
    base = concatenate_videoclips(scenes, method="compose")
    cap = captions_overlay(lines, seconds_per_line=seconds_per_line, font_preset=font_preset, box=True)
    video = CompositeVideoClip([base, cap]).set_fps(FPS)
    video = video.set_audio(trap_audio(video.duration))
    video.write_videofile(out, codec="libx264", audio_codec="aac", fps=FPS, bitrate="8000k")
    return out
