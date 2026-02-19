import { FindingsSummary, SecurityFinding } from "../types";

export type TimeSeriesPoint = {
  date: string;
  count: number;
};

export function countByDomain(findings: SecurityFinding[]): Array<{ domain: string; count: number }> {
  const totals = new Map<string, number>();
  for (const finding of findings) {
    const key = finding.domain || "other";
    totals.set(key, (totals.get(key) ?? 0) + 1);
  }
  return [...totals.entries()]
    .map(([domain, count]) => ({ domain, count }))
    .sort((a, b) => b.count - a.count);
}

export function countBySource(findings: SecurityFinding[]): Array<{ source: string; count: number }> {
  const totals = new Map<string, number>();
  for (const finding of findings) {
    const key = finding.source || "unknown";
    totals.set(key, (totals.get(key) ?? 0) + 1);
  }
  return [...totals.entries()]
    .map(([source, count]) => ({ source, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 8);
}

export function findingsTrend(findings: SecurityFinding[], days = 14): TimeSeriesPoint[] {
  const start = new Date();
  start.setHours(0, 0, 0, 0);
  start.setDate(start.getDate() - (days - 1));

  const buckets = new Map<string, number>();
  for (let i = 0; i < days; i += 1) {
    const date = new Date(start);
    date.setDate(start.getDate() + i);
    const key = date.toISOString().slice(0, 10);
    buckets.set(key, 0);
  }

  for (const finding of findings) {
    const key = new Date(finding.time).toISOString().slice(0, 10);
    if (buckets.has(key)) {
      buckets.set(key, (buckets.get(key) ?? 0) + 1);
    }
  }

  return [...buckets.entries()].map(([date, count]) => ({ date, count }));
}

export function executiveMetrics(summary: FindingsSummary, findings: SecurityFinding[]): {
  totalFindings: number;
  criticalRatio: string;
  averageRisk: string;
  distinctDomains: number;
} {
  const totalFindings = findings.length;
  const criticalRatio =
    totalFindings === 0 ? "0.0%" : `${((summary.critical / totalFindings) * 100).toFixed(1)}%`;
  const averageRisk =
    totalFindings === 0
      ? "0.0"
      : (findings.reduce((acc, finding) => acc + finding.risk_score, 0) / totalFindings).toFixed(1);
  const distinctDomains = new Set(findings.map((finding) => finding.domain)).size;

  return {
    totalFindings,
    criticalRatio,
    averageRisk,
    distinctDomains,
  };
}
