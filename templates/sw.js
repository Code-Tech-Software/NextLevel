
// Interceptar peticiones (Fetch)
const CACHE_NAME = 'mi-app-cache-v1';
const urlsToCache = [
  // Puedes dejar esto vacío por ahora
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

// NUEVA ESTRATEGIA: Network First (Red primero, luego caché)
self.addEventListener('fetch', event => {
  // Ignorar peticiones que no sean GET (como envíos de formularios en Django)
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Si la red funciona bien, devolvemos la respuesta de la red
        return response;
      })
      .catch(() => {
        // Si la red falla (estamos offline), buscamos en el caché
        return caches.match(event.request);
      })
  );
});