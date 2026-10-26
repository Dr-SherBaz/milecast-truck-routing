import { formatRisk, RISK_COLORS } from "@/lib/risk";
import type { RiskLevel } from "@/lib/types";

export function RiskBadge({ level }: { level: RiskLevel | string }) {
  const color = RISK_COLORS[(level as RiskLevel)] ?? "#64748b";
  return (
    <span className="risk-badge" style={{ ["--risk" as string]: color }}>
      {formatRisk(level)}
    </span>
  );
}
