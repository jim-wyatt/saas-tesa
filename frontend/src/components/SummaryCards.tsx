import { Grid2 as Grid, Paper, Typography } from "@mui/material";
import { alpha } from "@mui/material/styles";

import { executiveMetrics } from "../lib/insights";
import { SecurityFinding } from "../types";
import { FindingsSummary } from "../types";

type Props = {
  summary: FindingsSummary;
  findings: SecurityFinding[];
};

export function SummaryCards({ summary, findings }: Props): JSX.Element {
  const metrics = executiveMetrics(summary, findings);
  const items = [
    { label: "Total Findings", value: metrics.totalFindings, tone: "primary" as const },
    { label: "Critical Ratio", value: metrics.criticalRatio, tone: "error" as const },
    { label: "Average Risk", value: metrics.averageRisk, tone: "secondary" as const },
    { label: "Domains Covered", value: metrics.distinctDomains, tone: "info" as const },
    { label: "Low", value: summary.low, tone: "success" as const },
    { label: "Medium", value: summary.medium, tone: "warning" as const },
    { label: "High", value: summary.high, tone: "secondary" as const },
    { label: "Critical", value: summary.critical, tone: "error" as const },
  ];

  return (
    <Grid container spacing={2}>
      {items.map((item) => (
        <Grid key={item.label} size={{ xs: 12, sm: 6, md: 3, lg: 3 }}>
          <Paper
            sx={(theme) => ({
              p: 2,
              borderTop: 4,
              borderColor: theme.palette[item.tone].main,
              backgroundColor: alpha(theme.palette[item.tone].main, 0.06),
            })}
            elevation={0}
          >
            <Typography variant="body2" color="text.secondary">
              {item.label}
            </Typography>
            <Typography sx={(theme) => ({ color: theme.palette[item.tone].main })} variant="h4">
              {item.value}
            </Typography>
          </Paper>
        </Grid>
      ))}
    </Grid>
  );
}
