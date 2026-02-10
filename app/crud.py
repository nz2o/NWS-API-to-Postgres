from sqlalchemy.orm import Session
from . import models
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert
from dateutil import parser


def upsert_alert(db: Session, feature: dict):
    # extract ids and timestamps from feature
    nws_id = feature.get("id") or feature.get("properties", {}).get("id")
    properties = feature.get("properties", {})
    event = properties.get("event")
    status = properties.get("status")

    # parse timestamps if present
    def _parse(dt_str):
        if not dt_str:
            return None
        try:
            return parser.isoparse(dt_str)
        except Exception:
            return None

    sent_at = _parse(properties.get("sent"))
    effective_at = _parse(properties.get("effective"))
    onset_at = _parse(properties.get("onset"))
    expires_at = _parse(properties.get("expires"))
    ends_at = _parse(properties.get("ends"))
    updated_at = _parse(properties.get("updated"))

    if not nws_id:
        raise ValueError("feature missing id")

    # extract requested properties
    values = {
        "nws_id": nws_id,
        "event": event,
        "eventcode": properties.get("eventCode"),
        "headline": properties.get("headline"),
        "description": properties.get("description"),
        "instruction": properties.get("instruction"),
        "status": status,
        "message_type": properties.get("messageType"),
        "category": properties.get("category"),
        "severity": properties.get("severity"),
        "certainty": properties.get("certainty"),
        "urgency": properties.get("urgency"),
        "sender": properties.get("sender"),
        "sender_name": properties.get("senderName"),
        "sent_at": sent_at,
        "effective_at": effective_at,
        "onset_at": onset_at,
        "expires_at": expires_at,
        "ends_at": ends_at,
        "updated_at": updated_at,
        "area_desc": properties.get("areaDesc"),
        "geocode": properties.get("geocode"),
        "affected_zones": properties.get("affectedZones"),
        "references": properties.get("references"),
        "response": properties.get("response"),
        "parameters": properties.get("parameters"),
        "scope": properties.get("scope"),
        "code": properties.get("code"),
        "language": properties.get("language"),
        "web": properties.get("web"),
        "eventcode": properties.get("eventcode") or properties.get("eventCode"),
        "raw": feature,
    }

    stmt = insert(models.Alert).values(**values)

    # Update most fields on conflict to reflect any changes
    do_update = {k: getattr(stmt.excluded, k) for k in values.keys()}

    stmt = stmt.on_conflict_do_update(index_elements=[models.Alert.nws_id.key], set_=do_update)

    db.execute(stmt)
    db.commit()

    return db.query(models.Alert).filter_by(nws_id=nws_id).one()
