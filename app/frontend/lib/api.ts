import type { Plan } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function createPlan(input: {
  origin: string;
  destination: string;
  departure_time: string;
  load_weight_lb: number;
  checkpoint_interval_miles: number;
  forecast_offset_hours: number;
}): Promise<Plan> {
  const response = await fetch(`${API_URL}/api/plan`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(input) });
  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(payload?.detail ?? "Unable to build a route plan");
  }
  return response.json() as Promise<Plan>;
}
