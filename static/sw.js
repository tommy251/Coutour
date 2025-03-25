const CACHE_NAME = 'coutour-cache-v2'; // Updated cache name to force a refresh
const urlsToCache = [
    '/',
    '/static/styles.min.css',
    '/static/script.min.js'
    // Remove static image URLs since we'll cache them dynamically
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(urlsToCache);
            })
    );
    // Force the service worker to activate immediately
    self.skipWaiting();
});

self.addEventListener('activate', event => {
    // Clean up old caches
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    // Take control of the page immediately
    self.clients.claim();
});

self.addEventListener('fetch', event => {
    const requestUrl = new URL(event.request.url);

    // Cache static images dynamically
    if (requestUrl.pathname.startsWith('/static/') && /\.(webp|png|jpg|jpeg|gif)$/i.test(requestUrl.pathname)) {
        event.respondWith(
            caches.match(event.request)
                .then(response => {
                    // Return cached response if available
                    if (response) {
                        return response;
                    }
                    // Fetch from network and cache the response
                    return fetch(event.request)
                        .then(networkResponse => {
                            if (!networkResponse || networkResponse.status !== 200) {
                                return networkResponse;
                            }
                            return caches.open(CACHE_NAME)
                                .then(cache => {
                                    cache.put(event.request, networkResponse.clone());
                                    return networkResponse;
                                });
                        })
                        .catch(() => {
                            // Fallback for offline scenarios (optional)
                            return caches.match('/static/fallback.webp') || new Response('Image unavailable', { status: 404 });
                        });
                })
        );
    } else {
        // For non-image requests, use cache-first strategy
        event.respondWith(
            caches.match(event.request)
                .then(response => {
                    if (response) {
                        return response;
                    }
                    return fetch(event.request);
                })
        );
    }
});