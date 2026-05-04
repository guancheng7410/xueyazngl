var CACHE_NAME='bp-guardian-v1';
var ASSETS=[
    '/app_mobile.html',
    '/manifest.json'
];

self.addEventListener('install',function(e){
    e.waitUntil(
        caches.open(CACHE_NAME).then(function(cache){
            return cache.addAll(ASSETS);
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate',function(e){
    e.waitUntil(
        caches.keys().then(function(names){
            return Promise.all(
                names.filter(function(n){return n!==CACHE_NAME}).map(function(n){return caches.delete(n)})
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch',function(e){
    if(e.request.method!=='GET')return;
    
    e.respondWith(
        caches.match(e.request).then(function(r){
            return r||fetch(e.request).then(function(response){
                return caches.open(CACHE_NAME).then(function(cache){
                    cache.put(e.request,response.clone());
                    return response;
                });
            });
        }).catch(function(){
            if(e.request.headers.get('accept').includes('text/html')){
                return caches.match('/app_mobile.html');
            }
        })
    );
});

self.addEventListener('push',function(e){
    if(!e.data)return;
    var data=e.data.json();
    var opts={
        body:data.body||'您有一条新的提醒',
        icon:'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23667eea" width="100" height="100" rx="20"/><text x="50" y="68" text-anchor="middle" fill="white" font-size="55">🩺</text></svg>',
        badge:'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23667eea" width="100" height="100" rx="20"/><text x="50" y="68" text-anchor="middle" fill="white" font-size="55">🩺</text></svg>',
        tag:data.tag||'default',
        renotify:true,
        actions:[
            {action:'confirm',title:'确认服药'},
            {action:'dismiss',title:'稍后提醒'}
        ]
    };
    e.waitUntil(
        self.registration.showNotification(data.title||'血压守护',opts)
    );
});

self.addEventListener('notificationclick',function(e){
    e.notification.close();
    if(e.action==='confirm'){
        e.waitUntil(
            clients.matchAll({type:'window'}).then(function(ws){
                ws.forEach(function(w){w.postMessage({type:'confirm_med'})});
                if(ws.length===0)clients.openWindow('/app_mobile.html');
            })
        );
    }else{
        e.waitUntil(
            clients.openWindow('/app_mobile.html')
        );
    }
});
