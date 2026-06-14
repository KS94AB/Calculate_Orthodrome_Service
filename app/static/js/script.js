const form = document.getElementById("orthodromy-form");
const resultBlock = document.getElementById("result");

const map = L.map("map").setView([55, 30], 4);
map.attributionControl.setPrefix("Leaflet");

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "© OpenStreetMap"
}).addTo(map);

let currentLine = null;

function parseLinestring(wkt) {
    const coordinatesText = wkt
        .replace("LINESTRING(", "")
        .replace(")", "");

    const points = coordinatesText.split(",");

    return points.map(function (point) {
        const parts = point.trim().split(" ");
        const lon = Number(parts[0]);
        const lat = Number(parts[1]);

        return [lat, lon];
    });
}

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const point1 = document.getElementById("point1").value;
    const point2 = document.getElementById("point2").value;
    const cs = document.getElementById("cs").value;
    const count = document.getElementById("count").value;

    const params = new URLSearchParams({
        point1: point1,
        point2: point2,
        cs: cs,
        count: count,
        format: "json"
    });

    const response = await fetch(`/orthodromy?${params.toString()}`);

    if (!response.ok) {
        const errorText = await response.text();
        resultBlock.textContent = errorText;
        return;
    }

    const data = await response.json();

    resultBlock.textContent = data.wkt;

    const mapPoints = parseLinestring(data.map_wkt);

    if (currentLine !== null) {
        map.removeLayer(currentLine);
    }

    currentLine = L.polyline(mapPoints).addTo(map);

    map.fitBounds(currentLine.getBounds());
});