const CACHE_NAME = "biblioteca-pwa-shell-v1";
const CORE = ["./", "./index.html", "./manifest.webmanifest", "./icons/biblioteca-icon.svg"];
self.addEventListener("install", event => event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(CORE)).then(() => self.skipWaiting())));
self.addEventListener("activate", event => event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith("biblioteca-pwa-") && key !== CACHE_NAME).map(key => caches.delete(key)))).then(() => self.clients.claim())));
self.addEventListener("fetch", event => {
 const request = event.request;
 if (request.method !== "GET" || new URL(request.url).origin !== self.location.origin) return;
 if (request.mode === "navigate") event.respondWith(fetch(request).then(response => {
  if (response.ok) caches.open(CACHE_NAME).then(cache => cache.put(request, response.clone()));
  return response;
 }).catch(async () => (await caches.match(request)) || (await caches.match("./index.html"))));
});
