import { formatDuration } from "@/lib/risk";
import type { Route } from "@/lib/types";
import { RiskBadge } from "./RiskBadge";

export function RouteCard({ route, recommended }: { route: Route; recommended: boolean }) {
  const headline =
    route.summary.no_travel_miles > 0
      ? "no_travel"
      : route.summary.severe_miles > 0
        ? "severe"
        : route.summary.high_miles > 0
          ? "high"
          : "low";

  return (
    <article className={`route-card ${recommended ? "is-recommended" : ""}`}>
      <div className="card-top">
        <div>
          <p className="eyebrow">{recommended ? "Recommended" : "Alternative"}</p>
          <h3>{route.name}</h3>
        </div>
        <RiskBadge level={headline} />
      </div>
      <div className="route-stats">
        <span>
          <strong>{formatDuration(route.duration_minutes)}</strong> travel
        </span>
        <span>
          <strong>{route.distance_miles.toFixed(0)} mi</strong>
        </span>
        <span>
          <strong>{route.checkpoints.length}</strong> checks
        </span>
      </div>
      <div className="risk-grid">
        <div>
          <span>Severe</span>
          <strong>{route.summary.severe_miles.toFixed(0)} mi</strong>
        </div>
        <div>
          <span>High</span>
          <strong>{route.summary.high_miles.toFixed(0)} mi</strong>
        </div>
        <div>
          <span>No travel</span>
          <strong>{route.summary.no_travel_miles.toFixed(0)} mi</strong>
        </div>
        <div>
          <span>Avg risk</span>
          <strong>{route.summary.average_risk.toFixed(2)}</strong>
        </div>
      </div>
      <details>
        <summary>Checkpoint ETAs & risk</summary>
        <div className="checkpoint-list">
          {route.checkpoints.map((point) => (
            <div className="checkpoint-row" key={`${route.id}-${point.mile}`}>
              <span>
                {point.mile} mi ·{" "}
                {new Date(point.eta).toLocaleString([], {
                  month: "short",
                  day: "numeric",
                  hour: "numeric",
                  minute: "2-digit",
                })}
              </span>
              <RiskBadge level={point.risk_level} />
            </div>
          ))}
        </div>
      </details>
    </article>
  );
}
