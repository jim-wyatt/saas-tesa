import { Card, CardContent, CardHeader } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { countBySource } from "../lib/insights";
import { SecurityFinding } from "../types";

type Props = {
  findings: SecurityFinding[];
};

export function SourceChart({ findings }: Props): JSX.Element {
  const theme = useTheme();
  const data = countBySource(findings);

  return (
    <Card elevation={0} variant="outlined">
      <CardHeader title="Top Sources" subheader="Highest-volume producing controls/tools" />
      <CardContent sx={{ height: 320 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ left: 16, right: 16 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" allowDecimals={false} />
            <YAxis dataKey="source" type="category" width={110} />
            <Tooltip />
            <Bar dataKey="count" radius={[0, 4, 4, 0]} fill={theme.palette.primary.main} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
