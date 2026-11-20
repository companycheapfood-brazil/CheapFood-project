// CheapFood Service Worker - PWA Offline Caching
const CACHE_NAME = 'cheapfood-cache-v2';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/icon.svg',
  '/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  let url;
  try {
    url = new URL(req.url);
  } catch {
    return;
  }

  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;
  if (url.origin !== self.location.origin) return;
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/static/uploads/')) {
    return;
  }

  // Network first com fallback seguro para cache
  event.respondWith(
    fetch(req)
      .then((response) => {
        if (!response || response.status !== 200 || response.type !== 'basic') {
          return response;
        }
        const contentType = response.headers.get('content-type') || '';
        const isHtml = contentType.includes('text/html');
        // Nunca cacheia fallback HTML de SPA sob URLs de JS/CSS/ativos
        if (isHtml && req.mode !== 'navigate' && url.pathname !== '/' && url.pathname !== '/index.html') {
          return response;
        }
        const responseToCache = response.clone();
        const cacheKey = req.mode === 'navigate' ? '/index.html' : req;
        caches.open(CACHE_NAME)
          .then((cache) => cache.put(cacheKey, responseToCache))
          .catch(() => {});
        return response;
      })
      .catch(() => {
        return caches.match(req).then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          if (req.mode === 'navigate') {
            return caches.match('/index.html').then((fallback) => fallback || Response.error());
          }
          return Response.error();
        });
      })
  );
});
