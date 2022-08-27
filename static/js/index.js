var map = L.map('map', { zoomsliderControl: true, zoomControl: false }).setView([35.68066659206367, 139.7681614127473], 14);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

L.control.scale({imperial:false}).addTo(map);
L.Icon.Default.imagePath = 'https://unpkg.com/leaflet@1.3.1/dist/images/';