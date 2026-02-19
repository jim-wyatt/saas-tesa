import React from "react";
import ReactDOM from "react-dom/client";
import { CssBaseline, PaletteMode, ThemeProvider } from "@mui/material";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import App from "./App";
import { buildTheme } from "./theme";

const queryClient = new QueryClient();

function Root(): JSX.Element {
  const [mode, setMode] = React.useState<PaletteMode>(() => {
    const saved = window.localStorage.getItem("saastesa-theme-mode");
    return saved === "dark" ? "dark" : "light";
  });

  const theme = React.useMemo(() => buildTheme(mode), [mode]);

  const toggleTheme = React.useCallback(() => {
    setMode((prev) => {
      const next: PaletteMode = prev === "light" ? "dark" : "light";
      window.localStorage.setItem("saastesa-theme-mode", next);
      return next;
    });
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <QueryClientProvider client={queryClient}>
        <App mode={mode} onToggleTheme={toggleTheme} />
      </QueryClientProvider>
    </ThemeProvider>
  );
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>
);
