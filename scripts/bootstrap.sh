#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-up}"

require_cmd() {
	local cmd="$1"
	if ! command -v "$cmd" >/dev/null 2>&1; then
		echo "Missing required command: $cmd"
		exit 1
	fi
}

install_node_with_pkg_manager() {
	if ! command -v sudo >/dev/null 2>&1; then
		return 1
	fi

	if command -v apt-get >/dev/null 2>&1; then
		sudo apt-get update
		sudo apt-get install -y nodejs npm
		return 0
	fi

	if command -v dnf >/dev/null 2>&1; then
		sudo dnf install -y nodejs npm
		return 0
	fi

	if command -v yum >/dev/null 2>&1; then
		sudo yum install -y nodejs npm
		return 0
	fi

	if command -v pacman >/dev/null 2>&1; then
		sudo pacman -Sy --noconfirm nodejs npm
		return 0
	fi

	if command -v zypper >/dev/null 2>&1; then
		sudo zypper --non-interactive install nodejs npm
		return 0
	fi

	return 1
}

install_node_with_nvm() {
	require_cmd curl

	export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
	if [[ ! -s "$NVM_DIR/nvm.sh" ]]; then
		curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
	fi

	# shellcheck disable=SC1090
	. "$NVM_DIR/nvm.sh"
	nvm install --lts
	nvm use --lts
	hash -r
}

ensure_node_npm() {
	if command -v npm >/dev/null 2>&1 && command -v node >/dev/null 2>&1; then
		return 0
	fi

	echo "Node.js/npm not found. Attempting automatic installation..."

	if install_node_with_pkg_manager; then
		echo "Installed Node.js/npm via system package manager."
	elif install_node_with_nvm; then
		echo "Installed Node.js/npm via nvm."
	else
		echo "Unable to install Node.js/npm automatically."
		echo "Please install Node.js LTS and npm, then rerun scripts/bootstrap.sh."
		exit 1
	fi

	if ! command -v npm >/dev/null 2>&1 || ! command -v node >/dev/null 2>&1; then
		echo "Node.js/npm installation did not complete successfully."
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
	ensure_node_npm
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

run_live_reload() {
	cd "$ROOT_DIR"

	API_HOST="${TESA_API_HOST:-0.0.0.0}"
	API_PORT="${TESA_API_PORT:-8080}"
	FRONTEND_HOST="${TESA_FRONTEND_HOST:-0.0.0.0}"
	FRONTEND_PORT="${TESA_FRONTEND_PORT:-5173}"

	.venv/bin/python -m uvicorn saastesa.api.main:app \
		--host "$API_HOST" \
		--port "$API_PORT" \
		--reload \
		--reload-dir "$ROOT_DIR/src" &
	BACKEND_PID=$!

	(
		cd "$ROOT_DIR/frontend"
		npm run dev -- --host "$FRONTEND_HOST" --port "$FRONTEND_PORT"
	) &
	FRONTEND_PID=$!

	trap 'kill "$BACKEND_PID" "$FRONTEND_PID" >/dev/null 2>&1 || true' EXIT INT TERM

	echo "Backend live reload: http://$API_HOST:$API_PORT"
	echo "Frontend live reload: http://$FRONTEND_HOST:$FRONTEND_PORT"
	wait "$BACKEND_PID" "$FRONTEND_PID"
}

install_backend
install_frontend
seed_env_files

if [[ "$MODE" == "setup" ]]; then
	echo "Dev dependencies installed for backend and frontend."
	echo "Run: scripts/bootstrap.sh up"
	exit 0
fi

run_live_reload

