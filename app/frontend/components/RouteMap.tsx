"use client";

import { useEffect, useRef } from "react";
import type { Route } from "@/lib/types";

export function RouteMap({ routes, recommendedId }: { routes: Route[]; recommendedId: string }) {
  const mapRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    let map: import("leaflet").Map | undefined;
    let mounted = true;
    void import("leaflet").then((L) => {
      if (!mounted || !mapRef.current) return;
      map = L.map(mapRef.current, { zoomControl: false }).setView(routes[0]?.coordinates[0] ?? [39, -98], 4);
      L.control.zoom({ position: "bottomright" }).addTo(map);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: "© OpenStreetMap" }).addTo(map);
      const bounds = L.latLngBounds([]);
      routes.forEach((route) => {
        const line = L.polyline(route.coordinates, { color: route.id === recommendedId ? "#ef8354" : "#6b7280", weight: route.id === recommendedId ? 6 : 3, opacity: route.id === recommendedId ? 0.95 : 0.6 }).addTo(map!);
        line.bindTooltip(route.name);
        route.coordinates.forEach((point) => bounds.extend(point));
        route.checkpoints.forEach((checkpoint) => L.circleMarker([checkpoint.latitude, checkpoint.longitude], { radius: 5, color: riskColor(checkpoint.risk_level), fillColor: riskColor(checkpoint.risk_level), fillOpacity: 0.9, weight: 2 }).bindPopup(`<strong>${route.name} · ${checkpoint.mile} mi</strong><br/>${checkpoint.risk_level.replace("_", " ")} · ${checkpoint.weather.wind_mph} mph wind`).addTo(map!));
      });
      if (!bounds.isValid()) return;
      map.fitBounds(bounds, { padding: [24, 24] });
    });
    return () => { mounted = false; map?.remove(); };
  }, [routes, recommendedId]);
  return <div className="map-shell" ref={mapRef} aria-label="Map showing the three route alternatives and checkpoint risk markers" />;
}
function riskColor(level: string) { return ({ low: "#2f9e78", moderate: "#eab308", high: "#f97316", severe: "#dc2626", no_travel: "#7f1d1d" } as Record<string, string>)[level] ?? "#64748b"; }
