// 收租啦原生壳不再使用 PWA 缓存（由 index.html 启动时注销所有 SW）。
// 保留此文件仅为占位，不做任何缓存，所有请求直接放行。
self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', e => { /* 不拦截、不缓存 */ });
