import type { RiskLevel } from "./types";

export const RISK_COLORS: Record<RiskLevel, string> = {
  low: "#1f7a5c",
  moderate: "#c4a035",
  high: "#d97706",
  severe: "#c2410c",
  no_travel: "#7f1d1d",
};

export function formatRisk(level: string): string {
  return level.replaceAll("_", " ");
}

export function formatDuration(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const mins = Math.round(minutes % 60);
  if (hours <= 0) return `${mins}m`;
  return `${hours}h ${mins}m`;
}
