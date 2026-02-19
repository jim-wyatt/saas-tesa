#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEMO_COUNT="${TESA_DEMO_COUNT:-400}"
DEMO_DAYS="${TESA_DEMO_DAYS:-45}"

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd"
    exit 1
  fi
}

install_backend() {
  require_cmd python3
  cd "$ROOT_DIR"
  if [[ ! -d .venv ]]; then
    python3 -m venv .venv
  fi
  .venv/bin/python -m pip install --upgrade pip
  .venv/bin/python -m pip install -e .[dev]
}

install_frontend() {
  require_cmd npm
  cd "$ROOT_DIR/frontend"
  npm install
}

seed_env_files() {
  cd "$ROOT_DIR"
  if [[ ! -f .env && -f .env.example ]]; then
    cp .env.example .env
  fi
  if [[ ! -f frontend/.env && -f frontend/.env.example ]]; then
    cp frontend/.env.example frontend/.env
  fi
}

wait_for_http() {
  local url="$1"
  local name="$2"

  for _ in $(seq 1 90); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      echo "$name is ready: $url"
      return 0
    fi
    sleep 1
  done

  echo "Timed out waiting for $name at $url"
  return 1
}

open_dashboard() {
  local url="$1"
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$url" >/dev/null 2>&1 || true
  fi
}

run_demo() {
  require_cmd curl

  local api_bind_host="${TESA_API_HOST:-0.0.0.0}"
  local api_port="${TESA_API_PORT:-8080}"
  local frontend_bind_host="${TESA_FRONTEND_HOST:-0.0.0.0}"
  local frontend_port="${TESA_FRONTEND_PORT:-5173}"

  local api_url="http://localhost:${api_port}"
  local frontend_url="http://localhost:${frontend_port}"

  cd "$ROOT_DIR"

  .venv/bin/python -m uvicorn saastesa.api.main:app \
    --host "$api_bind_host" \
    --port "$api_port" \
    --reload \
    --reload-dir "$ROOT_DIR/src" &
  BACKEND_PID=$!

  (
    cd "$ROOT_DIR/frontend"
    npm run dev -- --host "$frontend_bind_host" --port "$frontend_port"
  ) &
  FRONTEND_PID=$!

  trap 'kill "$BACKEND_PID" "$FRONTEND_PID" >/dev/null 2>&1 || true' EXIT INT TERM

  wait_for_http "$api_url/health" "Backend API"
  wait_for_http "$frontend_url" "Frontend"

  .venv/bin/saastesa seed-demo --api-url "$api_url" --count "$DEMO_COUNT" --days "$DEMO_DAYS"

  echo ""
  echo "Executive demo mode is running"
  echo "- API: $api_url"
  echo "- Dashboard: $frontend_url"
  echo "- Seeded findings: $DEMO_COUNT over $DEMO_DAYS days"

  open_dashboard "$frontend_url"

  wait "$BACKEND_PID" "$FRONTEND_PID"
}

install_backend
install_frontend
seed_env_files
run_demo
