// Nombre del cache
const CACHE_NAME = 'ticket313-v1';

// Archivos a cachear en la instalación
const ASSETS_TO_CACHE = [
  '/',
  '/static/manifest.json',
  '/static/service-worker.js'
];

// Evento de instalación del service worker
self.addEventListener('install', event => {
  console.log('Service Worker: Instalando...');

  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('Service Worker: Cache abierto');
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );

  // Activar el service worker inmediatamente
  self.skipWaiting();
});

// Evento de activación del service worker
self.addEventListener('activate', event => {
  console.log('Service Worker: Activando...');

  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          // Eliminar caches antiguos
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: Eliminando cache antiguo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );

  // Controlar clientes inmediatamente
  self.clients.claim();
});

// Evento de fetch para cachear contenido dinámico
self.addEventListener('fetch', event => {
  // Solo cachear peticiones GET
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    caches.match(event.request).then(response => {
      // Si está en cache, devolverlo
      if (response) {
        return response;
      }

      // Si no está en cache, hacer la petición
      return fetch(event.request).then(response => {
        // Validar que la respuesta sea correcta
        if (!response || response.status !== 200 || response.type === 'error') {
          return response;
        }

        // Clonar la respuesta
        const responseToCache = response.clone();

        // Cachear la respuesta para peticiones GET exitosas
        if (event.request.method === 'GET' && response.status === 200) {
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }

        return response;
      }).catch(() => {
        // Si hay error de red, devolver una página offline
        return new Response(
          '<html><body><h1>Sin conexión</h1><p>Por favor, verifica tu conexión a internet.</p></body></html>',
          {
            headers: { 'Content-Type': 'text/html; charset=utf-8' }
          }
        );
      });
    })
  );
});
