const form = document.getElementById("orthodromy-form");
const resultBlock = document.getElementById("result");

const map = L.map("map").setView([55, 30], 4);
map.attributionControl.setPrefix("Leaflet");

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "© OpenStreetMap"
}).addTo(map);

function setupForbiddenZonesDrawing() {
    const forbiddenZones = new L.FeatureGroup();
    map.addLayer(forbiddenZones);

    const drawControl = new L.Control.Draw({
        edit: {
            featureGroup: forbiddenZones
        },
        draw: {
            polygon: true,
            marker: false,
            circle: false,
            circlemarker: false,
            rectangle: false,
            polyline: false
        }
    });

    map.addControl(drawControl);

    map.on(L.Draw.Event.CREATED, function (event) {
        const layer = event.layer;
        forbiddenZones.addLayer(layer);
    });

    return forbiddenZones;
}
const forbiddenZones = setupForbiddenZonesDrawing();

let currentLine = null;
let currentIntersections = [];

function clearIntersections() {
    for (const intersection of currentIntersections) {
        map.removeLayer(intersection);
    }

    currentIntersections = [];
}

function drawIntersections(intersectionsWkt) {
   clearIntersections();


    for (const wkt of intersectionsWkt) {
        const points = parseLinestring(wkt);
        const intersectionLine = L.polyline(points, {
            color: "red",
            weight: 6
        }).addTo(map);

        currentIntersections.push(intersectionLine);
    }
}

function parseLinestring(wkt) {
    const coordinatesText = wkt
        .trim()
        .replace(/^LINESTRING\s*\(/, "")
        .replace(/\)$/, "");

    const points = coordinatesText.split(",");

    return points.map(function (point) {
        const parts = point.trim().split(/\s+/);
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
    const forbiddenZonesGeoJson = forbiddenZones.toGeoJSON();
    const forbiddenZonesText = JSON.stringify(forbiddenZonesGeoJson);

    const params = new URLSearchParams({
    point1: point1,
    point2: point2,
    cs: cs,
    count: count,
    format: "json",
    forbidden_zones: forbiddenZonesText
    });

    const response = await fetch(`/orthodromy?${params.toString()}`);

    if (!response.ok) {
        const errorData = await response.json();

    resultBlock.textContent = errorData.error;
    if (errorData.map_wkt) {
    const mapPoints = parseLinestring(errorData.map_wkt);

    if (currentLine !== null) {
        map.removeLayer(currentLine);
    }

    currentLine = L.polyline(mapPoints).addTo(map);

    map.fitBounds(currentLine.getBounds());
}

        if (errorData.intersections_wkt) {
            drawIntersections(errorData.intersections_wkt);
    }
    return;
    }

    const data = await response.json();

    resultBlock.textContent = data.wkt;

    const mapPoints = parseLinestring(data.map_wkt);

    if (currentLine !== null) {
        map.removeLayer(currentLine);
    }
    clearIntersections();
    currentLine = L.polyline(mapPoints).addTo(map);
    map.fitBounds(currentLine.getBounds());
});