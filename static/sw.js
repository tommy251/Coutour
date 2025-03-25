const CACHE_NAME = 'coutour-cache-v1';
const urlsToCache = [
    '/',
    '/static/styles.min.css',
    '/static/script.min.js',
    '/static/Man.webp',
    '/static/men.webp',
    '/static/Blacksuit.webp'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});