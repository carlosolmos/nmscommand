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
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from model.dbmodels import Mission, Base, MissionStage, CheckListItem, MissionLogEntry

# Define the SQLAlchemy engine
engine = create_engine("sqlite:///nmscommand.db", echo=True)
# engine = create_engine("sqlite:///:memory:", echo=True)

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


# MissionLogEntry CRUD operations
def create_mission_log_entry(
    mission_id: str,
    log_entry: str,
    system_id: str,
    planet_id: str,
    planetbase_id: str,
    media: list[str],
) -> None:
    """Create a new mission log entry and add it to the database."""
    _new_log_entry = MissionLogEntry(
        mission_id=mission_id,
        log_entry=log_entry,
        system_id=system_id,
        planet_id=planet_id,
        planetbase_id=planetbase_id,
        media=media,
    )
    create_mission_log_entry_from_model(_new_log_entry)


def create_mission_log_entry_from_model(_new_log_entry: MissionLogEntry) -> None:
    """Create a new mission log entry and add it to the database."""
    session = create_session()
    session.add(_new_log_entry)
    session.commit()
    session.close()


def create_mission_log_entry_simple(mission_id: str, log_entry: str) -> None:
    """Create a new mission log entry and add it to the database."""
    _new_log_entry = MissionLogEntry(mission_id=mission_id, log_entry=log_entry)
    create_mission_log_entry_from_model(_new_log_entry)


def get_mission_log_entry_by_id(_id: int) -> Optional[MissionLogEntry]:
    """Get a mission log entry by its id."""
    _session = create_session()
    _log_entry = _session.query(MissionLogEntry).filter_by(id=_id).first()
    _session.close()
    return _log_entry


def get_all_mission_log_entries_by_mission_id(mission_id: str) -> list[MissionLogEntry]:
    """Get a list of mission log entries by mission id."""
    _session = create_session()
    _log_entries = (
        _session.query(MissionLogEntry)
        .filter_by(mission_id=mission_id)
        .order_by(desc(MissionLogEntry.created_at))
        .all()
    )
    _session.close()
    return _log_entries


def update_mission_log_entry(_session: Session, _id: int, log_entry: str) -> None:
    """Update a mission log entry."""
    local_session = False
    if _session is None:
        _session = create_session()
        local_session = True
    _log_entry = get_mission_log_entry_by_id(_session, _id)
    if _log_entry:
        _log_entry.log_entry = log_entry
        _session.commit()
    if local_session:
        _session.close()
