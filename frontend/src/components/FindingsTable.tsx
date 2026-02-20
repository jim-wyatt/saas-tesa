import { Card, CardContent, CardHeader, Chip } from "@mui/material";
import { DataGrid, GridColDef } from "@mui/x-data-grid";

import { SecurityFinding } from "../types";

type Props = {
  findings: SecurityFinding[];
};

const columns: GridColDef<SecurityFinding>[] = [
  { field: "title", headerName: "Title", flex: 1.3, minWidth: 220 },
  {
    field: "severity",
    headerName: "Severity",
    width: 120,
    renderCell: (params) => <Chip label={String(params.value)} size="small" variant="outlined" />,
  },
  { field: "risk_score", headerName: "Risk", width: 90, type: "number" },
  { field: "domain", headerName: "Domain", width: 140 },
  { field: "type_name", headerName: "Type", flex: 1.1, minWidth: 170 },
  { field: "source", headerName: "Source", width: 120 },
  {
    field: "time",
    headerName: "Observed",
    flex: 1.1,
    minWidth: 180,
    valueFormatter: (value) => new Date(value as string).toLocaleString(),
  },
  { field: "description", headerName: "Description", flex: 1.8, minWidth: 260 },
];

export function FindingsTable({ findings }: Props) {
  const rows = findings.map((finding, index) => ({ id: `${finding.title}-${index}`, ...finding }));

  return (
    <Card>
      <CardHeader title="Findings" />
      <CardContent sx={{ height: 520 }}>
        <DataGrid
          rows={rows}
          columns={columns}
          disableColumnMenu
          disableRowSelectionOnClick
          pageSizeOptions={[25, 50, 100]}
          initialState={{
            pagination: {
              paginationModel: { page: 0, pageSize: 25 },
            },
          }}
        />
      </CardContent>
    </Card>
  );
}
