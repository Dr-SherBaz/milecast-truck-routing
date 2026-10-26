import type { RiskLevel } from "@/lib/types";

const labels: Record<RiskLevel, string> = { low: "Low", moderate: "Moderate", high: "High", severe: "Severe", no_travel: "No travel" };
export function RiskBadge({ level }: { level: RiskLevel }) { return <span className={`risk risk-${level}`}>{labels[level]}</span>; }
