# DashGuard V9 Map Only

This build is intentionally boring and stable.

It has:
- No camera
- No TensorFlow
- No service worker / PWA cache
- Visible debug log
- GPS + OpenStreetMap only

## Run

```bash
python3 serve.py
```

Open the shown HTTPS URL on your iPhone in Safari.

Accept the self-signed certificate warning.

## First test

1. Tap `Load around address`.
   - Default is `64 Foley Road, Warwick, NY`.
   - Default radius is `2000` meters.
2. Confirm `OSM nodes loaded` is greater than 0.
3. Tap `Start GPS`.
4. Leave `Ignore heading filter for testing` checked first.
5. Drive or walk and watch:
   - Nearest raw
   - Ahead
   - Debug Log

Once counts look right, uncheck `Ignore heading filter for testing`.

## Why this version exists

The earlier version could get blocked by camera permission, TensorFlow model loading, or the service worker serving an old cached build. This one avoids all of that.
