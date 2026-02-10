import os
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from . import db, crud
from .models import Alert
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import httpx

API_URL = "https://api.weather.gov/alerts/active"

# Poll interval in seconds (configurable via environment / .env)
try:
    POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "60"))
except Exception:
    POLL_INTERVAL = 60

app = FastAPI(title="NWS to Postgres")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db_sess = db.SessionLocal()
    try:
        yield db_sess
    finally:
        db_sess.close()


@app.on_event("startup")
def startup():
    db.init_db()
    # start background poller
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(poller())
    except RuntimeError:
        # in some environments get_event_loop may fail; spawn task directly
        asyncio.create_task(poller())


async def poller():
    """Poll the NWS alerts feed every 60 seconds and upsert into Postgres."""
    async with httpx.AsyncClient(timeout=30) as client:
        while True:
            try:
                resp = await client.get(API_URL, headers={"Accept": "application/geo+json, application/json"})
                resp.raise_for_status()
                payload = resp.json()
                features = payload.get("features", []) or []
                # capture feed-level fetch metadata (including redirect chain)
                feed_fetch = {
                    "fetched_url": str(resp.url),
                    "status_code": resp.status_code,
                    "redirects": [str(h.url) for h in resp.history] if resp.history else [],
                }
                for feature in features:
                    # annotate each feature with feed fetch metadata
                    try:
                        feature["_feed_fetch"] = feed_fetch
                    except Exception:
                        pass
                    # run DB upsert in thread to avoid blocking the event loop
                    await asyncio.to_thread(process_feature, feature)
            except Exception as e:
                print("poller error:", e)
            await asyncio.sleep(POLL_INTERVAL)


def process_feature(feature: dict):
    db_sess = db.SessionLocal()
    try:
        # If feature 'id' looks like a URL, fetch that resource and record redirects/details.
        fid = feature.get("id")
        if isinstance(fid, str) and fid.startswith("http"):
            try:
                import httpx as _httpx
                r = _httpx.get(fid, follow_redirects=True, timeout=10, headers={"Accept": "application/geo+json, application/json"})
                detail = None
                try:
                    detail = r.json()
                except Exception:
                    detail = None
                feature["_detail_fetch"] = {
                    "fetched_url": str(r.url),
                    "status_code": r.status_code,
                    "redirects": [str(h.url) for h in r.history] if r.history else [],
                }
                if detail:
                    feature.setdefault("_detail", detail)
            except Exception as e:
                # don't fail processing a single feature because detail fetch failed
                feature.setdefault("_detail_fetch_error", str(e))

        crud.upsert_alert(db_sess, feature)
    except Exception as e:
        print("process_feature error:", e)
    finally:
        db_sess.close()


def _check_api_key(x_api_key: str | None = Header(None)) -> None:
    """Validate X-API-KEY header against ADMIN_API_KEY env var.

    Raises 401 if missing or invalid.
    """
    key = os.getenv("ADMIN_API_KEY")
    if not key:
        # Admin API key missing — disable the ingest endpoint explicitly.
        raise HTTPException(status_code=503, detail="Admin ingest endpoint is disabled: ADMIN_API_KEY not configured")
    if x_api_key != key:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/ingest/alerts", status_code=201)
def ingest_alert(payload: dict, db_sess: Session = Depends(get_db), _auth: None = Depends(_check_api_key)):
    """Authenticated endpoint to insert/upsert alerts into Postgres.

    Provide `X-API-KEY` header matching `ADMIN_API_KEY`.
    """
    try:
        alert = crud.upsert_alert(db_sess, payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"id": alert.id}


@app.get("/alerts")
def list_alerts(limit: int = 10, db_sess: Session = Depends(get_db)):
    rows = db_sess.query(Alert).order_by(Alert.id.desc()).limit(limit).all()
    return [
        {
            "id": r.id,
            "nws_id": r.nws_id,
            "event": r.event,
            "status": r.status,
            "sent_at": r.sent_at.isoformat() if r.sent_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            "raw": r.raw,
        }
        for r in rows
    ]
