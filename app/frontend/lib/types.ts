export type RiskLevel = "low" | "moderate" | "high" | "severe" | "no_travel";

export type Checkpoint = {
  mile: number;
  latitude: number;
  longitude: number;
  eta: string;
  forecast_offset_hours: number;
  weather: { wind_mph: number; rain_in_hr: number; snow_in_hr: number; temperature_f: number };
  risk_level: RiskLevel;
  risk_score: number;
  risk_reasons: string[];
};

export type Route = {
  id: string;
  name: string;
  distance_miles: number;
  duration_minutes: number;
  coordinates: [number, number][];
  checkpoints: Checkpoint[];
  summary: { low_miles: number; moderate_miles: number; high_miles: number; severe_miles: number; no_travel_miles: number; average_risk: number };
};

export type Plan = {
  request: { origin: string; destination: string; departure_time: string; load_weight_lb: number; checkpoint_interval_miles: number; forecast_offset_hours: number };
  routes: Route[];
  recommended_route_id: string;
  recommendation_reason: string;
  corridor_heatmap: Checkpoint[];
  forecast_window_hours: number;
};
