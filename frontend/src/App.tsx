import { DarkMode, LightMode } from "@mui/icons-material";
import { Alert, Box, CircularProgress, Container, Grid, IconButton, Stack, Typography } from "@mui/material";
import { alpha } from "@mui/material/styles";
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { SpeedInsights } from "@vercel/speed-insights/react";

import { API_BASE_URL, getFindings, getSummary } from "./api";
import { DomainChart } from "./components/DomainChart";
import { FindingsChart } from "./components/FindingsChart";
import { FindingsTable } from "./components/FindingsTable";
import { SourceChart } from "./components/SourceChart";
import { SummaryCards } from "./components/SummaryCards";
import { TrendChart } from "./components/TrendChart";

type Props = {
  mode: "light" | "dark";
  onToggleTheme: () => void;
};

export default function App({ mode, onToggleTheme }: Props) {
  const [loadingWarning, setLoadingWarning] = useState(false);

  const {
    data: summary,
    isLoading: summaryLoading,
    isError: summaryError,
    error: summaryErrorDetails,
  } = useQuery({ queryKey: ["summary"], queryFn: getSummary, refetchInterval: 15000 });

  const {
    data: findings,
    isLoading: findingsLoading,
    isError: findingsError,
    error: findingsErrorDetails,
  } = useQuery({ queryKey: ["findings"], queryFn: () => getFindings(500), refetchInterval: 15000 });

  useEffect(() => {
    const timer = window.setTimeout(() => setLoadingWarning(true), 10000);
    return () => window.clearTimeout(timer);
  }, []);

  const getErrorMessage = (error: unknown): string => {
    if (error instanceof Error) {
      return error.message;
    }
    return "Unknown error";
  };

  if (summaryLoading || findingsLoading) {
    return (
      <Container sx={{ py: 4 }}>
        <Box sx={{ minHeight: "30vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <CircularProgress />
        </Box>
        {loadingWarning ? (
          <Alert severity="warning" sx={{ mt: 2 }}>
            Still loading data from {API_BASE_URL}. If this persists, check API reachability and CORS settings.
          </Alert>
        ) : null}
      </Container>
    );
  }

  if (summaryError || findingsError || !summary || !findings) {
    return (
      <Container sx={{ py: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          Unable to load SaaS TESA data from the API.
        </Alert>
        <Alert severity="info">
          API base URL: {API_BASE_URL}
          <br />
          Summary error: {getErrorMessage(summaryErrorDetails)}
          <br />
          Findings error: {getErrorMessage(findingsErrorDetails)}
        </Alert>
      </Container>
    );
  }

  return (
    <Container
      maxWidth="xl"
      sx={(theme) => ({
        py: 4,
        background: `linear-gradient(180deg, ${alpha(theme.palette.primary.main, 0.08)} 0%, ${alpha(
          theme.palette.background.default,
          0.98
        )} 32%)`,
      })}
    >
      <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}>
        <Stack direction="row" spacing={1.5} alignItems="center">
          <Box
            component="img"
            src="/favicon.svg"
            alt="SaaS TESA icon"
            sx={{ width: 44, height: 44, borderRadius: 1.5, boxShadow: 2 }}
          />
          <Box>
            <Typography color="primary" variant="h4" gutterBottom>
              SaaS TESA Dashboard
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Threat Environment Situational Awareness for SaaS engineering organizations.
            </Typography>
          </Box>
        </Stack>
        <IconButton color="primary" onClick={onToggleTheme} aria-label="toggle color mode">
          {mode === "light" ? <DarkMode /> : <LightMode />}
        </IconButton>
      </Stack>

      <Grid container spacing={3}>
        <Grid size={12}>
          <SummaryCards summary={summary} findings={findings} />
        </Grid>
        <Grid size={{ xs: 12, md: 6, lg: 4 }}>
          <FindingsChart summary={summary} />
        </Grid>
        <Grid size={{ xs: 12, md: 6, lg: 4 }}>
          <DomainChart findings={findings} />
        </Grid>
        <Grid size={{ xs: 12, lg: 4 }}>
          <SourceChart findings={findings} />
        </Grid>
        <Grid size={{ xs: 12, lg: 5 }}>
          <TrendChart findings={findings} />
        </Grid>
        <Grid size={{ xs: 12, lg: 7 }}>
          <FindingsTable findings={findings} />
        </Grid>
      </Grid>
      <SpeedInsights />
    </Container>
  );
}
