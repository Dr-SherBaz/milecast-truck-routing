"use client";

import { FormEvent, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { createPlan } from "@/lib/api";
import type { Plan } from "@/lib/types";
import { ForecastSlider } from "@/components/ForecastSlider";
import { RouteCard } from "@/components/RouteCard";
import { RouteMap } from "@/components/RouteMap";

function defaultDeparture(): string {
  const value = new Date(Date.now() + 60 * 60 * 1000);
  value.setMinutes(0, 0, 0);
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${value.getFullYear()}-${pad(value.getMonth() + 1)}-${pad(value.getDate())}T${pad(value.getHours())}:00`;
}

export default function Home() {
  const [origin, setOrigin] = useState("Denver, CO");
  const [destination, setDestination] = useState("Chicago, IL");
  const [departure, setDeparture] = useState(defaultDeparture);
  const [weight, setWeight] = useState("28000");
  const [interval, setIntervalMiles] = useState("25");
  const [offset, setOffset] = useState(0);
  const [plan, setPlan] = useState<Plan | null>(null);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");
  const [activeRouteId, setActiveRouteId] = useState<string | undefined>();
  const hasPlan = useRef(false);
  const formRef = useRef({ origin, destination, departure, weight, interval });
  formRef.current = { origin, destination, departure, weight, interval };

  const build = useCallback(async (nextOffset: number, mode: "submit" | "slider") => {
    const form = formRef.current;
    if (mode === "submit") setLoading(true);
    else setRefreshing(true);
    setError("");
    try {
      const next = await createPlan({
        origin: form.origin,
        destination: form.destination,
        departure_time: new Date(form.departure).toISOString(),
        load_weight_lb: Number(form.weight),
        checkpoint_interval_miles: Number(form.interval),
        forecast_offset_hours: nextOffset,
      });
      setPlan(next);
      setActiveRouteId(next.recommended_route_id);
      hasPlan.current = true;
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Unable to build a plan");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  function onSubmit(event: FormEvent) {
    event.preventDefault();
    void build(offset, "submit");
  }

  useEffect(() => {
    if (!hasPlan.current) return;
    const timer = window.setTimeout(() => {
      void build(offset, "slider");
    }, 450);
    return () => window.clearTimeout(timer);
  }, [offset, build]);

  const recommended = useMemo(
    () => plan?.routes.find((route) => route.id === plan.recommended_route_id),
    [plan],
  );

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">M</span>
          <div>
            <p className="brand-name">Milecast</p>
            <p className="brand-tag">Weather-timed freight corridors</p>
          </div>
        </div>
        <p className="stack-pill">React + Django · live providers</p>
      </header>

      <section className="intro">
        <div>
          <p className="eyebrow">Spotter assessment build</p>
          <h1>Safest route for this load, this weather, this departure.</h1>
          <p className="lede">
            Three alternatives. Weather sampled every 10, 25, or 50 miles at the truck&apos;s ETA.
            Ranked by severe miles, high miles, average risk, then time.
          </p>
        </div>
      </section>

      <section className="workspace">
        <form className="panel form" onSubmit={onSubmit}>
          <div className="panel-head">
            <h2>Trip inputs</h2>
            <span>01</span>
          </div>
          <div className="pair">
            <label>
              Origin
              <input value={origin} onChange={(e) => setOrigin(e.target.value)} required />
            </label>
            <label>
              Destination
              <input value={destination} onChange={(e) => setDestination(e.target.value)} required />
            </label>
          </div>
          <div className="pair">
            <label>
              Departure date & time
              <input type="datetime-local" value={departure} onChange={(e) => setDeparture(e.target.value)} required />
            </label>
            <label>
              Load weight (lb)
              <input type="number" min={1} max={100000} value={weight} onChange={(e) => setWeight(e.target.value)} required />
            </label>
          </div>
          <label>
            Checkpoint spacing
            <select value={interval} onChange={(e) => setIntervalMiles(e.target.value)}>
              <option value="10">Every 10 miles</option>
              <option value="25">Every 25 miles</option>
              <option value="50">Every 50 miles</option>
            </select>
          </label>
          <ForecastSlider value={offset} onChange={setOffset} disabled={loading} />
          <button className="primary" type="submit" disabled={loading}>
            {loading ? "Planning corridors…" : "Build weather-aware plan"}
          </button>
          {refreshing && <p className="status">Refreshing corridor forecast…</p>}
          {error && (
            <p className="error" role="alert">
              {error}
            </p>
          )}
        </form>

        <aside className="panel rules">
          <p className="eyebrow">PDF risk rules</p>
          <h2>Wind, rain, snow, load.</h2>
          <ul>
            <li>
              <strong>Wind</strong> &lt;25 low · 25–34 mod · 35–44 high · 45–54 severe · ≥55 no travel
            </li>
            <li>
              <strong>Rain</strong> thresholds to &gt;1.00 in/hr no travel
            </li>
            <li>
              <strong>Snow</strong> thresholds to &gt;3.0 in/hr no travel
            </li>
            <li>
              <strong>Load</strong> 45–54 mph + &gt;30k lb = no travel · 35–44 + &gt;40k = severe
            </li>
          </ul>
        </aside>
      </section>

      {plan && (
        <section className="results">
          <div className="results-head">
            <div>
              <p className="eyebrow">Corridor comparison</p>
              <h2>Three routes · +{plan.request.forecast_offset_hours}h forecast</h2>
              <p className="muted">
                {plan.request.resolved_origin ?? plan.request.origin}
                {" → "}
                {plan.request.resolved_destination ?? plan.request.destination}
              </p>
            </div>
            <div className="rec">
              <span>Recommended</span>
              <strong>{recommended?.name}</strong>
            </div>
          </div>

          <div className="result-grid">
            <div className="map-column">
              <RouteMap
                routes={plan.routes}
                recommendedId={plan.recommended_route_id}
                activeRouteId={activeRouteId}
              />
              <div className="legend">
                <span>
                  <i className="swatch low" /> Low
                </span>
                <span>
                  <i className="swatch moderate" /> Moderate
                </span>
                <span>
                  <i className="swatch high" /> High
                </span>
                <span>
                  <i className="swatch severe" /> Severe
                </span>
                <span>
                  <i className="swatch no_travel" /> No travel
                </span>
              </div>
            </div>
            <div className="cards">
              {plan.routes.map((route) => (
                <div
                  key={route.id}
                  role="button"
                  tabIndex={0}
                  onClick={() => setActiveRouteId(route.id)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" || event.key === " ") setActiveRouteId(route.id);
                  }}
                >
                  <RouteCard route={route} recommended={route.id === plan.recommended_route_id} />
                </div>
              ))}
            </div>
          </div>

          <div className="reason">
            <strong>{plan.recommendation_reason}</strong>
            <p>Heatmap colors follow checkpoint risk along each corridor. Slider shifts the 0–48 hour window.</p>
          </div>
        </section>
      )}

      <footer className="footer">
        <span>Milecast · independent Spotter assessment implementation</span>
        <span>Nominatim · OSRM/ORS · Open-Meteo</span>
      </footer>
    </main>
  );
}
