# NWS → Postgres ⚡️

Minimal FastAPI service that receives NWS alerts and stores them in Postgres.

See [installation instructions](./install.md) for installation and run instructions. 🚀

Notes

- ⚠️ Work in progress: use at your own risk. Probably doesn't even work!
- ⚙️ Configuration is done via environment variables; see `install.md` and `.env`.

Files

- 🐳 `Dockerfile`, `docker-compose.yml` - container setup
- 📦 `requirements.txt` - Python deps
- 🧩 `app/` - FastAPI application and DB models
