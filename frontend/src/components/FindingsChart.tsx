import { Card, CardContent, CardHeader } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { FindingsSummary } from "../types";

type Props = {
  summary: FindingsSummary;
};

export function FindingsChart({ summary }: Props) {
  const theme = useTheme();
  const data = [
    { severity: "Low", count: summary.low, color: theme.palette.success.main },
    { severity: "Medium", count: summary.medium, color: theme.palette.warning.main },
    { severity: "High", count: summary.high, color: theme.palette.secondary.main },
    { severity: "Critical", count: summary.critical, color: theme.palette.error.main },
  ];

  return (
    <Card elevation={0} variant="outlined">
      <CardHeader title="Severity Distribution" subheader="Normalized risk bucket counts" />
      <CardContent sx={{ height: 320 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="severity" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="count" radius={[4, 4, 0, 0]}>
              {data.map((entry) => (
                <Cell key={entry.severity} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
