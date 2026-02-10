import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Require DATABASE_URL to be explicitly provided for security.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")

# Create engine with pool_pre_ping to avoid stale connections.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Fail fast: attempt a simple connection to validate credentials/access.
try:
    conn = engine.connect()
    conn.close()
except SQLAlchemyError as e:
    raise RuntimeError(f"Unable to connect to the database: {e}")

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def init_db():
    # create tables
    Base.metadata.create_all(bind=engine)
    # seed default emoji mappings if tables are empty
    try:
        from . import models
        from datetime import datetime

        session = SessionLocal()
        try:
            if session.query(models.SeverityEmoji).count() == 0:
                defaults = [
                    models.SeverityEmoji(severity="Extreme", emoji="🚨", description="Extreme severity"),
                    models.SeverityEmoji(severity="Severe", emoji="🔴", description="Severe severity"),
                    models.SeverityEmoji(severity="Moderate", emoji="🟠", description="Moderate severity"),
                    models.SeverityEmoji(severity="Minor", emoji="🟡", description="Minor severity"),
                    models.SeverityEmoji(severity="Unknown", emoji="❓", description="Unknown severity"),
                ]
                session.add_all(defaults)

            if session.query(models.PhenomenonEmoji).count() == 0:
                phenos = [
                    models.PhenomenonEmoji(phenomenon="Flooding", emoji="🌊", description="Flooding"),
                    models.PhenomenonEmoji(phenomenon="Flash Flood", emoji="🌊", description="Flash Flood"),
                    models.PhenomenonEmoji(phenomenon="Coastal Flood", emoji="🌊🏖️", description="Coastal Flood"),
                    models.PhenomenonEmoji(phenomenon="Storm Surge", emoji="🌊⚠️", description="Storm Surge"),
                    models.PhenomenonEmoji(phenomenon="Tornado", emoji="🌪️", description="Tornado"),
                    models.PhenomenonEmoji(phenomenon="Hurricane", emoji="🌀", description="Hurricane / Tropical Cyclone"),
                    models.PhenomenonEmoji(phenomenon="Tropical Storm", emoji="🌀", description="Tropical Storm"),
                    models.PhenomenonEmoji(phenomenon="High Wind", emoji="💨", description="High Wind"),
                    models.PhenomenonEmoji(phenomenon="Wind", emoji="🌬️", description="Wind"),
                    models.PhenomenonEmoji(phenomenon="Hail", emoji="🧊", description="Hail"),
                    models.PhenomenonEmoji(phenomenon="Severe Thunderstorm", emoji="⛈️⚠️", description="Severe Thunderstorm"),
                    models.PhenomenonEmoji(phenomenon="Thunderstorm", emoji="⛈️", description="Thunderstorm"),
                    models.PhenomenonEmoji(phenomenon="Lightning", emoji="⚡", description="Lightning"),
                    models.PhenomenonEmoji(phenomenon="Heat", emoji="🥵", description="Heat"),
                    models.PhenomenonEmoji(phenomenon="Extreme Heat", emoji="🔥", description="Extreme Heat"),
                    models.PhenomenonEmoji(phenomenon="Cold", emoji="🥶", description="Cold"),
                    models.PhenomenonEmoji(phenomenon="Freeze", emoji="🧊", description="Freeze"),
                    models.PhenomenonEmoji(phenomenon="Frost", emoji="🧊❄️", description="Frost"),
                    models.PhenomenonEmoji(phenomenon="Wind Chill", emoji="🥶💨", description="Wind Chill"),
                    models.PhenomenonEmoji(phenomenon="Snow", emoji="❄️", description="Snow"),
                    models.PhenomenonEmoji(phenomenon="Blizzard", emoji="🌨️❄️", description="Blizzard"),
                    models.PhenomenonEmoji(phenomenon="Sleet", emoji="🌨️🧊", description="Sleet"),
                    models.PhenomenonEmoji(phenomenon="Freezing Rain", emoji="🌧️🧊", description="Freezing Rain"),
                    models.PhenomenonEmoji(phenomenon="Rip Current", emoji="🏊‍♂️🚫", description="Rip Current"),
                    models.PhenomenonEmoji(phenomenon="Dense Fog", emoji="🌫️", description="Dense Fog"),
                    models.PhenomenonEmoji(phenomenon="Dense Smoke", emoji="🌫️🔥", description="Dense Smoke"),
                    models.PhenomenonEmoji(phenomenon="Smoke", emoji="💨🔥", description="Smoke"),
                    models.PhenomenonEmoji(phenomenon="Fire", emoji="🔥", description="Wildfire / Fire"),
                    models.PhenomenonEmoji(phenomenon="Avalanche", emoji="🏔️❄️", description="Avalanche"),
                    models.PhenomenonEmoji(phenomenon="Landslide", emoji="🌋🧱", description="Landslide"),
                    models.PhenomenonEmoji(phenomenon="Dust Storm", emoji="🌪️🌫️", description="Dust Storm"),
                    models.PhenomenonEmoji(phenomenon="Sandstorm", emoji="🏜️🌫️", description="Sandstorm"),
                    models.PhenomenonEmoji(phenomenon="Earthquake", emoji="🌎⚠️", description="Earthquake"),
                    models.PhenomenonEmoji(phenomenon="Tsunami", emoji="🌊⚠️", description="Tsunami"),
                    models.PhenomenonEmoji(phenomenon="Volcano", emoji="🌋", description="Volcanic Activity"),
                    models.PhenomenonEmoji(phenomenon="Coastal Hazard", emoji="🏖️⚠️", description="Coastal Hazard"),
                    models.PhenomenonEmoji(phenomenon="Marine Hazard", emoji="⛵⚠️", description="Marine Hazard"),
                    models.PhenomenonEmoji(phenomenon="Ice Accretion", emoji="🧊❄️", description="Ice Accretion"),
                    models.PhenomenonEmoji(phenomenon="Debris Flow", emoji="🧱🌊", description="Debris Flow"),
                ]
                session.add_all(phenos)

            session.commit()
        finally:
            session.close()
    except Exception:
        # Seeding should not prevent the app from starting; log if available.
        pass
