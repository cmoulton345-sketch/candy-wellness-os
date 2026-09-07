# SOP: Prospect Video Recording & Sharing
**Category:** Operations | **Version:** 1.0 | **Last Updated:** March 2026

---

## What This Does
Records a personal video message (screen + face cam) for a prospect and delivers it as a shareable public link — no Loom subscription required.

**Result:** A professional, branded video link you can paste into any follow-up email within 5 minutes.

---

## Tools Required
- **Clipchamp** — built into Windows 11 (free, no install needed)
- **Cloudflare R2** — `flowstatesocialimages` bucket (already set up)
- Your webcam + microphone

---

## When to Use This
- After a discovery call where they said "maybe" — send a personal recap video
- Before a call to pre-warm a cold lead
- As a follow-up to a proposal
- To re-engage a prospect who went quiet

---

## Steps

### Step 1 — Open Clipchamp
Press `Win` and search **"Clipchamp"** → open it

### Step 2 — Start a New Recording
1. Click **"Record yourself"** or **"Create a new video"**
2. Select **"Screen and camera"** mode
3. Position your face cam bubble (bottom corner looks best)
4. Do a 5-second test before recording for real

### Step 3 — Record Your Video
**Keep it under 2 minutes.** Use this structure:

```
[0:00–0:15]  Hi [Name], it's Joe from FlowstateAI...
[0:15–0:45]  Here's exactly what I'd build for [Business Name]...
[0:45–1:30]  Here's why it matters for you specifically...
[1:30–1:50]  Next step is simple — [call to action]
[1:50–2:00]  Looking forward to it / talk soon
```

### Step 4 — Export the Video
1. Click **"Export"** → choose **1080p**
2. Clipchamp saves the `.mp4` to your Downloads folder
3. Rename it immediately:
```
flowstateai-[firstname]-[businessname].mp4
Example: flowstateai-sarah-coastal-dental.mp4
```
4. Move it to: `C:\Users\Admin\Videos\Prospects\`

### Step 5 — Upload to Cloudflare R2
1. Go to **dash.cloudflare.com** → R2 → `flowstatesocialimages`
2. Click the **Objects** tab
3. Click **Upload** → select your `.mp4`
4. Upload path: `prospects/flowstateai-sarah-coastal-dental.mp4`

### Step 6 — Get the Public Link
1. Click the uploaded file
2. Copy the **Public URL** — it looks like:
```
https://pub-949f9709a419448187860a08ec5938c3.r2.dev/prospects/flowstateai-sarah-coastal-dental.mp4
```

### Step 7 — Paste Into Your Email
Drop the link into your follow-up email. Example:

> I put together a quick 90-second walkthrough of exactly what I'd build for [Business Name]:
>
> 👉 [your link here]
>
> No pitch — just showing you the system before you commit to anything.

---

## Pro Tips
- **Look at the camera**, not your screen — feels more personal
- **Say their name in the first 5 seconds** — it hooks immediately
- **Don't re-record more than twice** — authentic > perfect
- Use the same video structure every time — it gets faster

---

## File Organization
```
C:\Users\Admin\Videos\Prospects\
└── flowstateai-[firstname]-[businessname].mp4

R2 Bucket: flowstatesocialimages
└── prospects/
    └── flowstateai-[firstname]-[businessname].mp4
```

---

*FlowstateAI Automation — Operations SOP*
