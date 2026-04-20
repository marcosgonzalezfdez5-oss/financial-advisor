#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# Financial Advisor — Project Setup Script
# ─────────────────────────────────────────────

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✓ $*${NC}"; }
warn() { echo -e "${YELLOW}⚠ $*${NC}"; }
fail() { echo -e "${RED}✗ $*${NC}"; exit 1; }

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Investment Research Agent — Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── 1. Check prerequisites ─────────────────────

echo "Checking prerequisites..."

command -v docker >/dev/null 2>&1 || fail "Docker not found. Install Docker Desktop: https://www.docker.com/products/docker-desktop"
ok "Docker found: $(docker --version | head -1)"

command -v uv >/dev/null 2>&1 || {
    warn "uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
}
ok "uv found: $(uv --version)"

# ── 2. Create .env if missing ──────────────────

if [ ! -f "$ROOT/.env" ]; then
    cp "$ROOT/.env.example" "$ROOT/.env"
    warn ".env created from .env.example"
    warn "ACTION REQUIRED: Open .env and set your ANTHROPIC_API_KEY before continuing."
    echo ""
    read -rp "  Press Enter once you have set ANTHROPIC_API_KEY in .env..."
else
    ok ".env already exists"
fi

# Check that ANTHROPIC_API_KEY is not the placeholder
if grep -q "your-anthropic-api-key-here" "$ROOT/.env"; then
    fail "ANTHROPIC_API_KEY is still the placeholder value. Edit .env before running setup."
fi

# ── 3. Install Python dependencies ────────────

echo ""
echo "Installing Python dependencies..."
uv sync
ok "Dependencies installed"

# ── 4. Start PostgreSQL ────────────────────────

echo ""
echo "Starting PostgreSQL container..."
docker compose up -d db
ok "Container started"

# ── 5. Wait for PostgreSQL to be healthy ───────

echo ""
echo "Waiting for PostgreSQL to be ready..."
RETRIES=20
until docker compose exec -T db pg_isready -U postgres -d financial_advisor >/dev/null 2>&1; do
    RETRIES=$((RETRIES - 1))
    if [ "$RETRIES" -le 0 ]; then
        fail "PostgreSQL did not become ready in time. Check: docker compose logs db"
    fi
    echo "  Waiting... ($RETRIES attempts left)"
    sleep 2
done
ok "PostgreSQL is ready"

# ── 6. Create database tables ─────────────────

echo ""
echo "Initialising database tables..."
uv run python scripts/init_db.py
ok "Database tables created"

# ── Done ───────────────────────────────────────

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}  Setup complete!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Start the API server:"
echo ""
echo "    uv run uvicorn api.main:app --reload --port 8000"
echo ""
echo "  API docs available at:"
echo "    http://localhost:8000/docs"
echo ""
echo "  Stop PostgreSQL when done:"
echo "    docker compose down"
echo ""
