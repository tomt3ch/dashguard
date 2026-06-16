# DashGuard — Setup Guide

## Files
- `index.html` — the full app
- `manifest.json` — PWA install metadata
- `sw.js` — service worker (offline caching)
- `icons/` — home screen icons
- `serve.py` — local HTTPS server (required for GPS + camera on iPhone)

---

## Requirements
- Python 3 (built into Mac, comes with most Linux)
- `openssl` (built into Mac)
- iPhone + computer on the **same Wi-Fi network**
- Internet for first load (caches TF model + OSM data after that)

---

## Step 1 — Start the server

```bash
cd ~/Downloads/dashguard
python3 serve.py
```

You'll see:
```
Open on your iPhone: https://192.168.1.42:8443
```

---

## Step 2 — Open in Safari on iPhone

1. Type the URL into **Safari** (must be Safari for GPS + PWA install)
2. You'll see a certificate warning — tap **Advanced → Proceed**
   *(it's your own server, this is safe)*
3. Tap **Allow Camera & GPS — Start**
4. Grant Camera permission when prompted
5. Grant Location permission when prompted — choose **"Allow While Using App"**

---

## Step 3 — Mount and drive

- Mount your iPhone on the dash pointing out the windshield
- Plug into 12V USB adapter for power
- Volume **all the way up** (not silent/vibrate mode)
- The map layer starts warning you as soon as GPS locks (~10 seconds)
- Camera layer runs simultaneously as verification

---

## Understanding the display

**Status bar (top):**
- `GPS ±5m` — GPS locked, accuracy shown
- `OSM: 12 nodes` — map data loaded, number of signs in 600m radius
- `Detecting` — camera model running

**Alert cards (bottom of camera view):**
- `MAP` badge (blue) — sign from OpenStreetMap data only
- `CAM` badge (amber) — sign from camera only (not in map data)
- `MAP+CAM` badge (green) — both sources agree (highest confidence)
- Distance in feet, colour-coded: gray=far, amber=medium, red=close

**Voice alerts fire at:** 500ft, 400ft, 300ft, 200ft, 150ft, 100ft, 50ft

---

## Troubleshooting

| Problem | Fix |
|---|---|
| GPS not locking | Go outside/near window. Takes ~10s cold start. |
| "OSM failed" | Check internet. Overpass API is free but rate-limited. |
| Camera denied | Safari → AA → Website Settings → Camera → Allow |
| Location denied | Settings → Privacy → Location Services → Safari → While Using |
| No voice | Phone not on silent. Tap screen first (iOS needs gesture). |
| Can't reach server | Same Wi-Fi? Try disabling Mac firewall temporarily. |

---

## Phase 3 (coming next)
- Full offline cache — pre-download OSM tiles for a route before driving
- Red/yellow/green traffic light colour detection
- Raspberry Pi port with local YOLO model
