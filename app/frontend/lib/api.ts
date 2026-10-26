import type { Plan, PlanInput } from "./types";

// Empty = same-origin (Next.js rewrites to Django). Set NEXT_PUBLIC_API_URL for split deploys.
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "";

function formatDetail(payload: unknown): string {
  if (!payload || typeof payload !== "object") {
    return "Unable to build a route plan";
  }
  const data = payload as Record<string, unknown>;
  if (typeof data.detail === "string") return data.detail;
  if (Array.isArray(data.detail)) {
    return data.detail
      .map((item) => (typeof item === "object" && item && "msg" in item ? String((item as { msg: string }).msg) : String(item)))
      .join("; ");
  }
  const fieldErrors = Object.entries(data)
    .filter(([, value]) => Array.isArray(value))
    .map(([key, value]) => `${key}: ${(value as string[]).join(", ")}`);
  if (fieldErrors.length) return fieldErrors.join("; ");
  return "Unable to build a route plan";
}

export async function createPlan(input: PlanInput): Promise<Plan> {
  const response = await fetch(`${API_URL}/api/plan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(formatDetail(payload));
  }
  return payload as Plan;
}
