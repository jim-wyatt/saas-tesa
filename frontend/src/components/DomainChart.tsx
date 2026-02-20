import { Card, CardContent, CardHeader } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { SecurityFinding } from "../types";
import { countByDomain } from "../lib/insights";

type Props = {
  findings: SecurityFinding[];
};

export function DomainChart({ findings }: Props) {
  const theme = useTheme();
  const data = countByDomain(findings);

  return (
    <Card elevation={0} variant="outlined">
      <CardHeader title="Findings by Domain" subheader="Application, infrastructure, and adjacent domains" />
      <CardContent sx={{ height: 320 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="domain" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="count" radius={[4, 4, 0, 0]} fill={theme.palette.info.main} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
