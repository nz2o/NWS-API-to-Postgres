import traceback
from app.db import SessionLocal
from app import crud


def main():
    feature = {
        "id": "test-alert-1",
        "type": "Feature",
        "properties": {
            "event": "Unit Test Alert",
            "eventCode": {"SAME": ["TST"]},
            "headline": "Unit test headline",
            "description": "This is a test alert inserted by integration test.",
            "instruction": "No action required.",
            "status": "Actual",
            "messageType": "Alert",
            "category": "Test",
            "severity": "Unknown",
            "certainty": "Unknown",
            "urgency": "Unknown",
            "sender": "test@example.local",
            "senderName": "UnitTest",
            "sent": "2026-02-11T00:00:00Z",
            "effective": "2026-02-11T00:00:00Z",
            "expires": "2026-02-11T01:00:00Z",
            "areaDesc": "Test Area",
            "geocode": {"SAME": ["000000"]},
            "affectedZones": [],
            "references": [],
            "parameters": {"TEST": ["1"]},
        },
    }

    session = SessionLocal()
    try:
        alert = crud.upsert_alert(session, feature)
        print("OK: inserted/updated alert id=", alert.id)
    except Exception as e:
        print("ERROR during upsert:")
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    main()
