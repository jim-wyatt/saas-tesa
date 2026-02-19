import { PaletteMode, createTheme } from "@mui/material";

export function buildTheme(mode: PaletteMode) {
  return createTheme({
    palette: {
      mode,
      primary: {
        main: mode === "light" ? "#005A9C" : "#4DA3FF",
      },
      secondary: {
        main: mode === "light" ? "#7A1FA2" : "#C792EA",
      },
      info: {
        main: mode === "light" ? "#0288D1" : "#4FC3F7",
      },
      success: {
        main: mode === "light" ? "#2E7D32" : "#81C784",
      },
      warning: {
        main: mode === "light" ? "#ED6C02" : "#FFB74D",
      },
      error: {
        main: mode === "light" ? "#D32F2F" : "#EF9A9A",
      },
      background: {
        default: mode === "light" ? "#F7F9FC" : "#12004A",
        paper: mode === "light" ? "#FFFFFF" : "#1A0A58",
      },
    },
    shape: {
      borderRadius: 10,
    },
  });
}
