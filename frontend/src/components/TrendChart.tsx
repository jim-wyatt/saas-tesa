import { Card, CardContent, CardHeader } from "@mui/material";
import { alpha, useTheme } from "@mui/material/styles";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { findingsTrend } from "../lib/insights";
import { SecurityFinding } from "../types";

type Props = {
  findings: SecurityFinding[];
};

export function TrendChart({ findings }: Props): JSX.Element {
  const theme = useTheme();
  const data = findingsTrend(findings, 14);

  return (
    <Card elevation={0} variant="outlined">
      <CardHeader title="14-Day Trend" subheader="Daily finding volume" />
      <CardContent sx={{ height: 320 }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="count"
              stroke={theme.palette.secondary.main}
              fill={alpha(theme.palette.secondary.main, 0.2)}
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
