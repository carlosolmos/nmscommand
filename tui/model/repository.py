"""Persistence layer"""

import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
import jsons

from datetime import datetime
from typing import Optional
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.dbmodels import Mission, Base, MissionStage, CheckListItem

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
    _m_milestones = []
    if len(milestones) > 0:
        _m_milestones = [CheckListItem(item, False) for item in milestones]

    _m_swag = []
    if len(swag) > 0:
        _m_swag = [CheckListItem(item, False) for item in swag]

    _m_tech = []
    if len(tech) > 0:
        _m_tech = [CheckListItem(item, False) for item in tech]

    _m_resources = []
    if len(resources) > 0:
        _m_resources = [CheckListItem(item, False) for item in resources]

    _new_mission = Mission(
        codename=codename,
        description=description,
        start_date=start_date,
        end_date=end_date,
        stage=stage,
        milestones=jsons.dump(_m_milestones),
        swag=jsons.dump(_m_swag),
        tech=jsons.dump(_m_tech),
        resources=jsons.dump(_m_resources),
        media=media,
    )
    create_mission_from_model(_new_mission)
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
    _session = create_session()
    _mission = _session.query(Mission).filter_by(codename=codename).first()
    _session.close()
    return _mission


def get_mission_by_id(_id: int) -> Optional[Mission]:
    """Get a mission by its id."""
    _session = create_session()
    _mission = _session.query(Mission).filter_by(id=_id).first()
    _session.close()
    return _mission


def get_missions_active(_session: Session) -> list[Mission]:
    """Get a list of active missions."""
    _session = create_session()
    _missions = (
        _session.query(Mission).filter(Mission.stage < MissionStage.Complete).all()
    )
    _session.close()
    return _missions


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
