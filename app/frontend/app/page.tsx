"use client";

import { FormEvent, useMemo, useState } from "react";
import { createPlan } from "@/lib/api";
import type { Plan } from "@/lib/types";
import { ForecastSlider } from "@/components/ForecastSlider";
import { RouteCard } from "@/components/RouteCard";
import { RouteMap } from "@/components/RouteMap";

const initialDeparture = new Date(Date.now() + 60 * 60 * 1000);
initialDeparture.setMinutes(0, 0, 0);
const localDateTime = `${initialDeparture.getFullYear()}-${String(initialDeparture.getMonth() + 1).padStart(2, "0")}-${String(initialDeparture.getDate()).padStart(2, "0")}T${String(initialDeparture.getHours()).padStart(2, "0")}:00`;

export default function Home() {
  const [origin, setOrigin] = useState("Denver, CO");
  const [destination, setDestination] = useState("Chicago, IL");
  const [departure, setDeparture] = useState(localDateTime);
  const [weight, setWeight] = useState("28000");
  const [interval, setInterval] = useState("25");
  const [offset, setOffset] = useState(0);
  const [plan, setPlan] = useState<Plan | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setLoading(true); setError("");
    try { setPlan(await createPlan({ origin, destination, departure_time: new Date(departure).toISOString(), load_weight_lb: Number(weight), checkpoint_interval_miles: Number(interval), forecast_offset_hours: offset })); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Unable to build a plan"); }
    finally { setLoading(false); }
  }

  const recommended = useMemo(() => plan?.routes.find((route) => route.id === plan.recommended_route_id), [plan]);
  return <main><header className="topbar"><div className="brand-mark">R</div><div><p className="brand">ROUTEWISE</p><p className="brand-subtitle">Weather intelligence for long haul</p></div><span className="mode-pill"><i /> Local planning mode</span></header><section className="hero"><div className="hero-copy"><p className="eyebrow">Safety-first dispatch</p><h1>Know the road<br /><em>before you roll.</em></h1><p>Compare three route alternatives against the weather your truck will actually encounter at every checkpoint.</p></div><div className="hero-note"><span className="note-icon">✦</span><div><strong>Decision support, not a guarantee</strong><p>Always verify live conditions and official road advisories before departure.</p></div></div></section><section className="planner-grid"><form className="panel planning-form" onSubmit={submit}><div className="panel-heading"><div><p className="eyebrow">Trip setup</p><h2>Plan a safer route</h2></div><span className="step">01 / 01</span></div><div className="form-row"><label>Origin<input value={origin} onChange={(e) => setOrigin(e.target.value)} placeholder="City, state" required /></label><span className="route-arrow">→</span><label>Destination<input value={destination} onChange={(e) => setDestination(e.target.value)} placeholder="City, state" required /></label></div><div className="form-row two"><label>Departure date & time<input type="datetime-local" value={departure} onChange={(e) => setDeparture(e.target.value)} required /></label><label>Load weight <span className="unit">lb</span><input type="number" min="1" max="100000" value={weight} onChange={(e) => setWeight(e.target.value)} required /></label></div><div className="form-row two"><label>Checkpoint spacing<select value={interval} onChange={(e) => setInterval(e.target.value)}><option value="10">Every 10 miles</option><option value="25">Every 25 miles</option><option value="50">Every 50 miles</option></select></label><div className="provider-note"><span>◎</span><span>Mock providers active<br /><small>No API keys required</small></span></div></div><ForecastSlider value={offset} onChange={setOffset} /><button className="primary-button" type="submit" disabled={loading}>{loading ? "Building your plan…" : "Build route plan  →"}</button>{error && <p className="error-message" role="alert">{error}</p>}</form><aside className="panel rules-panel"><p className="eyebrow">How risk is scored</p><h2>Four signals.<br />One clear call.</h2><div className="rule"><span className="rule-icon wind">↝</span><div><strong>Wind</strong><p>35+ mph raises risk. 55+ means no travel.</p></div></div><div className="rule"><span className="rule-icon rain">◒</span><div><strong>Rain & snow</strong><p>Precipitation intensity is measured at ETA.</p></div></div><div className="rule"><span className="rule-icon load">▣</span><div><strong>Load weight</strong><p>Heavy loads tighten the wind thresholds.</p></div></div><div className="rule"><span className="rule-icon rank">↗</span><div><strong>Route priority</strong><p>Severe miles → high miles → average risk → time.</p></div></div></aside></section>{plan && <section className="results"><div className="results-heading"><div><p className="eyebrow">Live comparison</p><h2>Your route intelligence</h2><p className="muted">{plan.routes.length} alternatives · Checkpoints every {plan.request.checkpoint_interval_miles} miles · Forecast offset +{plan.request.forecast_offset_hours}h</p></div><div className="recommendation"><span className="recommendation-dot" /><div><small>Recommended route</small><strong>{recommended?.name}</strong></div></div></div><div className="result-layout"><div className="map-column"><RouteMap routes={plan.routes} recommendedId={plan.recommended_route_id} /><div className="map-legend"><span><i className="legend-line recommended-line" />Recommended</span><span><i className="legend-line" />Alternative</span><span><i className="legend-dot low-dot" />Low</span><span><i className="legend-dot severe-dot" />Severe</span></div></div><div className="route-list">{plan.routes.map((route) => <RouteCard key={route.id} route={route} recommended={route.id === plan.recommended_route_id} />)}</div></div><div className="insight-banner"><span className="insight-symbol">✦</span><div><strong>{plan.recommendation_reason}</strong><p>Recommendation follows the assessment priority order. Review every checkpoint before dispatch.</p></div></div><div className="heatmap-section"><div><p className="eyebrow">Corridor weather heatmap</p><h3>Risk intensity by checkpoint</h3></div><div className="heatmap-strip">{plan.corridor_heatmap.slice(0, 36).map((point, index) => <div key={`${point.mile}-${index}`} className={`heat-cell heat-${point.risk_level}`} title={`${point.mile} mi · ${point.risk_level}`} />)}</div><div className="heatmap-labels"><span>Origin</span><span>Low risk</span><span>High / severe</span><span>Destination</span></div></div></section>}<footer><span>ROUTEWISE / Weather-aware dispatch intelligence</span><span>Assessment build · Mock data mode</span></footer></main>;
}
