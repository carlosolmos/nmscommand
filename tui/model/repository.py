"""Persistence layer"""

import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from datetime import datetime
from typing import Optional
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.dbmodels import Mission, Base

# Define the SQLAlchemy engine
# engine = create_engine('sqlite:///nmscommand.db', echo=True)
engine = create_engine("sqlite:///:memory:", echo=True)

# Create the database tables
Base.metadata.create_all(engine)


def create_session():
    """Define a function to create a new session"""
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# Example CRUD operations


# Create
def create_mission(
    session,
    codename: str,
    description: str,
    start_date: datetime,
    end_date: datetime,
    stage: int,
    milestones: list[str],
    swag: list[str],
    tech: list[str],
    resources: list[str],
    media: list[str],
) -> Mission:
    """Create a new mission and add it to the database."""
    local_session = False
    if session is None:
        session = create_session()
        local_session = True

    _new_mission = Mission(
        codename=codename,
        description=description,
        start_date=start_date,
        end_date=end_date,
        stage=stage,
        milestones=milestones,
        swag=swag,
        tech=tech,
        resources=resources,
        media=media,
    )
    session.add(_new_mission)
    session.commit()
    if local_session:
        session.close()

    return _new_mission


def create_mission_from_model(_new_mission: Mission) -> Mission:
    """Create a new mission and add it to the database."""
    session = create_session()
    session.add(_new_mission)
    session.commit()
    session.close()
    return _new_mission


# Read
def get_mission_by_codename(_session: Session, codename: str) -> Optional[Mission]:
    """Get a mission by its codename."""
    local_session = False
    if _session is None:
        _session = create_session()
        local_session = True
    _mission = _session.query(Mission).filter_by(codename=codename).first()
    return _mission


# Update
def update_mission_stage(_session: Session, codename: str, new_stage: int) -> None:
    """Update the stage of a mission."""
    local_session = False
    if _session is None:
        _session = create_session()
        local_session = True
    _mission = get_mission_by_codename(_session, codename)
    if _mission:
        _mission.stage = new_stage
        _session.commit()
    if local_session:
        _session.close()


# Delete
def delete_mission(_session: Session, codename: str) -> None:
    """Delete a mission by its codename."""
    local_session = False
    if _session is None:
        _session = create_session()
        local_session = True
    _mission = get_mission_by_codename(_session, codename)
    if _mission:
        _session.delete(_mission)
        _session.commit()
    if local_session:
        _session.close()


# Example usage
if __name__ == "__main__":
    print("Running example usage")
    # Create a session
    session = create_session()

    # Create a new mission
    new_mission = create_mission(
        session,
        codename="Mission1",
        description="First mission",
        start_date=datetime.now(),
        end_date=datetime.now(),
        stage=1,
        milestones=["milestone1", "milestone2"],
        swag=["swag1", "swag2"],
        tech=["tech1", "tech2"],
        resources=["resource1", "resource2"],
        media=["media1", "media2"],
    )

    # Read the mission
    mission = get_mission_by_codename(session, "Mission1")
    print("Mission:", mission.codename, mission.description)

    # Update the mission stage
    update_mission_stage(session, "Mission1", 2)

    # Read the updated mission
    mission = get_mission_by_codename(session, "Mission1")
    print("Updated Stage:", mission.stage)

    # Delete the mission
    delete_mission(session, "Mission1")

    # Close the session
    session.close()
