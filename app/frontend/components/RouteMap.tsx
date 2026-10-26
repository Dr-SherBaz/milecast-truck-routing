"use client";

import { useEffect, useRef } from "react";
import { RISK_COLORS } from "@/lib/risk";
import type { RiskLevel, Route } from "@/lib/types";

type Props = {
  routes: Route[];
  recommendedId: string;
  activeRouteId?: string;
};

export function RouteMap({ routes, recommendedId, activeRouteId }: Props) {
  const mapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let map: import("leaflet").Map | undefined;
    let mounted = true;

    void import("leaflet").then((L) => {
      if (!mounted || !mapRef.current) return;

      map = L.map(mapRef.current, { zoomControl: false, attributionControl: true }).setView(
        routes[0]?.coordinates[0] ?? [39.5, -98],
        5,
      );
      L.control.zoom({ position: "bottomright" }).addTo(map);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
        maxZoom: 18,
      }).addTo(map);

      const bounds = L.latLngBounds([]);
      const focusId = activeRouteId ?? recommendedId;

      routes.forEach((route) => {
        const isFocus = route.id === focusId;
        const base = L.polyline(route.coordinates, {
          color: isFocus ? "#1c2b3a" : "#94a3b8",
          weight: isFocus ? 7 : 4,
          opacity: isFocus ? 0.35 : 0.25,
          lineCap: "round",
        }).addTo(map!);
        base.bindTooltip(route.name);
        route.coordinates.forEach((point) => bounds.extend(point));

        // Corridor heatmap: color each checkpoint-to-checkpoint segment by risk.
        const points = route.checkpoints;
        for (let index = 0; index < points.length; index += 1) {
          const current = points[index];
          const previous = index === 0
            ? { latitude: route.coordinates[0][0], longitude: route.coordinates[0][1], risk_level: current.risk_level as RiskLevel }
            : points[index - 1];
          const segment: [number, number][] = [
            [previous.latitude, previous.longitude],
            [current.latitude, current.longitude],
          ];
          L.polyline(segment, {
            color: RISK_COLORS[current.risk_level],
            weight: isFocus ? 6 : 3,
            opacity: isFocus ? 0.95 : 0.55,
            lineCap: "round",
          }).addTo(map!);

          L.circleMarker([current.latitude, current.longitude], {
            radius: isFocus ? 6 : 4,
            color: "#0f172a",
            weight: 1,
            fillColor: RISK_COLORS[current.risk_level],
            fillOpacity: 0.95,
          })
            .bindPopup(
              `<strong>${route.name}</strong><br/>${current.mile} mi · ${current.risk_level.replace("_", " ")}` +
                `<br/>${current.weather.wind_mph} mph wind · rain ${current.weather.rain_in_hr} in/hr` +
                `<br/>ETA ${new Date(current.eta).toLocaleString()}`,
            )
            .addTo(map!);
        }
      });

      if (bounds.isValid()) {
        map.fitBounds(bounds, { padding: [36, 36] });
      }
    });

    return () => {
      mounted = false;
      map?.remove();
    };
  }, [routes, recommendedId, activeRouteId]);

  return <div className="map-shell" ref={mapRef} aria-label="Route corridor weather heatmap" />;
}
