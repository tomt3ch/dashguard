const CACHE = 'dashguard-v2';

// App shell — cached at install time
const APP_SHELL = [
  './index.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
];

// CDN hosts whose responses we cache aggressively (TF.js model weights)
const CDN_CACHE_HOSTS = [
  'cdn.jsdelivr.net',
  'unpkg.com',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // CDN model files — cache-first, these are large and never change
  if (CDN_CACHE_HOSTS.includes(url.hostname)) {
    e.respondWith(
      caches.match(e.request).then(hit => {
        if (hit) return hit;
        return fetch(e.request).then(res => {
          // Only cache successful responses
          if (res.ok) {
            const clone = res.clone();
            caches.open(CACHE).then(c => c.put(e.request, clone));
          }
          return res;
        });
      })
    );
    return;
  }

  // Nominatim lookups — network only, never cache (location-specific, short-lived)
  if (url.hostname === 'nominatim.openstreetmap.org') {
    e.respondWith(fetch(e.request));
    return;
  }

  // Overpass API — network only during downloads; live queries handled by app logic
  if (url.hostname === 'overpass-api.de') {
    e.respondWith(fetch(e.request));
    return;
  }

  // App shell — cache-first with background network update
  e.respondWith(
    caches.match(e.request).then(hit => {
      const networkFetch = fetch(e.request).then(res => {
        if (res.ok) {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      }).catch(() => null);
      return hit || networkFetch;
    })
  );
});
