/* Service Worker：离线缓存刷题应用（PWA）v2 —— 网络优先策略 */
const CACHE = "fire-quiz-v2";
const ASSETS = [
  "./index.html",
  "./manifest.json",
  "./icon-192.png",
  "./icon-512.png"
];

// 安装：预缓存核心资源
self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

// 激活：清理旧缓存（v1 等）
self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// 请求：网络优先（在线拿最新版并更新缓存；离线回退缓存）
self.addEventListener("fetch", (e) => {
  // 只处理同源 GET（不代理跨域请求）
  if (e.request.method !== "GET" || !e.request.url.startsWith(self.location.origin)) return;
  e.respondWith(
    fetch(e.request)
      .then((res) => {
        // 成功响应写入缓存（下次离线可用）
        if (res && res.status === 200) {
          const clone = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, clone));
        }
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
