# Install & Run 🛠️

Copy `.env` and set secure values (or edit `DATABASE_URL` directly):

```bash
cp .env .env.local
# edit .env.local and set DATABASE_URL, POSTGRES_* and APP_PORT as needed
```

Prerequisites ✅

- Docker Desktop (macOS/Windows): https://www.docker.com/products/docker-desktop/
- Docker Engine (Linux): https://docs.docker.com/engine/install/
- (Optional) Portainer for managing containers on Linux: https://www.portainer.io/

Build and run with Docker Compose:

```bash
docker-compose up --build
```

By default the app maps the container port `8000` to the host port configured by `APP_PORT` (default `18080`).

# Install & Run 🛠️

Copy `.env` and set secure values (or edit `DATABASE_URL` directly): 📝

```bash
cp .env .env.local
# edit .env.local and set DATABASE_URL, POSTGRES_* and APP_PORT as needed
```

Prerequisites ✅

- 🐳 Docker Desktop (macOS/Windows): https://www.docker.com/products/docker-desktop/
- 🐧 Docker Engine (Linux): https://docs.docker.com/engine/install/
- 🧭 (Optional) Portainer for managing containers on Linux: https://www.portainer.io/

Build and run with Docker Compose ▶️

```bash
docker-compose up --build
```

By default the app maps the container port `8000` to the host port configured by `APP_PORT` (default `18080`). 📍

API examples 🚧

List recent alerts (public, read-only):

```bash
curl http://localhost:18080/alerts
```

Authenticated ingest (admin)

To insert alerts via API (separate from the public read endpoint) use the authenticated ingest endpoint. 🔐

Set a strong `ADMIN_API_KEY` in your `.env` and call:

```bash
curl -X POST http://localhost:18080/ingest/alerts \
  -H 'Content-Type: application/json' \
  -H 'X-API-KEY: <your-admin-key>' \
  -d '{"id":"https://api.weather.gov/alerts/1","properties":{"event":"Test","sent":"2026-02-09T12:00:00Z"}}'
```

Note: the public `/alerts` endpoint is read-only.

Environment variables 🔧

- `DATABASE_URL` (required)
- `APP_PORT` (optional, default 18080)
- `POLL_INTERVAL` (seconds, default 60)
- `ADMIN_API_KEY` (recommended; required to enable `/ingest/alerts`) 🔑

If you run an external Postgres/PostGIS instance, set `DATABASE_URL` to point at it. The app will fail fast if `DATABASE_URL` is not set or is unreachable.
PY
```

Postgres (Docker Compose) notes 🗄️

- Image: this repo's `docker-compose.yml` uses `postgis/postgis:18`, which includes PostGIS extensions.
- Ports: you can control the host/container mapping with `POSTGRES_HOST_PORT` (host side) and `POSTGRES_PORT` (container side). Defaults are `5432`.
- Data directory / volume: Postgres 18 recommends using `PGDATA=/var/lib/postgresql/data/pgdata` for the database cluster directory. The compose file maps the named volume `db_data` to that `PGDATA` path to avoid permission/initialization issues. Using a named volume is strongly recommended over binding a host directory directly; if you must bind-mount a host path, ensure correct ownership and permissions for the Postgres user.

Example `.env` entries (optional — only set values you want to override):

```
# Postgres ports
POSTGRES_HOST_PORT=5432
POSTGRES_PORT=5432

# Postgres credentials (defaults used by compose if omitted - CHANGE THESE!)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=nws
```

The app's default `DATABASE_URL` in `docker-compose.yml` points at the `db` service and uses the container port; if you change `POSTGRES_HOST_PORT`, update `DATABASE_URL` accordingly when connecting from the host (for example: `postgresql+psycopg2://user:pass@localhost:${POSTGRES_HOST_PORT}/nws`).

Windows (PowerShell):

```powershell
# Using PowerShell with .NET RNG
[Convert]::ToBase64String((New-Object System.Security.Cryptography.RNGCryptoServiceProvider).GetBytes(32))

# Or, if Python is installed (recommended for cross-platform):
python - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
```

Add the generated secret to `.env`:

```text
ADMIN_API_KEY=your-generated-secret-here
```

Export/set the variable for a one-off run (Linux/macOS):

```bash
export ADMIN_API_KEY=your-generated-secret-here
docker-compose up --build
```

Windows (PowerShell):

```powershell
$env:ADMIN_API_KEY = 'your-generated-secret-here'
docker-compose up --build
```

If you run an external Postgres/PostGIS instance, set `DATABASE_URL` to point at it. The app will fail fast if `DATABASE_URL` is not set or is unreachable.
