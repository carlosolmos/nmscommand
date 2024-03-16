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
from sqlalchemy.orm import sessionmaker, lazyload
from model.dbmodels import Mission, Base, MissionStage, CheckListItem, MissionLogEntry

# Define the SQLAlchemy engine
engine = create_engine(
    "sqlite:///nmscommand.db",
    echo=True,
)
# engine = create_engine("sqlite:///:memory:", echo=True)
session_maker = sessionmaker(bind=engine)
session = session_maker()

# Create the database tables
Base.metadata.create_all(engine)


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
    # session.begin()
    session.add(_new_mission)
    session.commit()
    return _new_mission


# Read
def get_mission_by_codename(codename: str) -> Optional[Mission]:
    """Get a mission by its codename."""
    _mission = session.query(Mission).filter_by(codename=codename).first()
    return _mission


def get_mission_by_id(_id: int) -> Optional[Mission]:
    """Get a mission by its id."""
    _mission = session.query(Mission).filter_by(id=_id).first()
    return _mission


def get_missions_active() -> list[Mission]:
    """Get a list of active missions."""
    _missions = session.query(Mission).filter(Mission.stage < MissionStage.Complete).all()
    return _missions


# Update


def update_mission(
    mission_id: str,
    codename: str,
    description: str,
    start_date: datetime,
) -> None:
    """Update a mission."""
    _mission = get_mission_by_id(mission_id)
    if _mission:
        _mission.codename = codename
        _mission.description = description
        _mission.start_date = start_date
        session.commit()
    else:
        print(f"Mission with id {mission_id} not found.")


def update_mission_stage(codename: str, new_stage: int) -> None:
    """Update the stage of a mission."""
    # session.begin()
    _mission = get_mission_by_codename(codename)
    if _mission:
        _mission.stage = new_stage
        session.commit()


# Delete
def delete_mission(codename: str) -> None:
    """Delete a mission by its codename."""
    # session.begin()
    _mission = get_mission_by_codename(codename)
    if _mission:
        session.delete(_mission)
        session.commit()


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
    # session.begin()
    session.add(_new_log_entry)
    session.commit()


def create_mission_log_entry_simple(mission_id: str, log_entry: str) -> None:
    """Create a new mission log entry and add it to the database."""
    _new_log_entry = MissionLogEntry(mission_id=mission_id, log_entry=log_entry)
    create_mission_log_entry_from_model(_new_log_entry)


def get_mission_log_entry_by_id(_id: int) -> Optional[MissionLogEntry]:
    """Get a mission log entry by its id."""
    _log_entry = session.query(MissionLogEntry).filter_by(id=_id).first()
    return _log_entry


def get_last_mission_log_entry() -> Optional[MissionLogEntry]:
    """Get the last mission log entry."""
    _log_entry = (
        session.query(MissionLogEntry)
        .options(lazyload(MissionLogEntry.mission))
        .order_by(desc(MissionLogEntry.created_at))
        .first()
    )
    return _log_entry


def get_all_mission_log_entries_by_mission_id(mission_id: str) -> list[MissionLogEntry]:
    """Get a list of mission log entries by mission id."""
    _log_entries = (
        session.query(MissionLogEntry)
        .filter_by(mission_id=mission_id)
        .order_by(desc(MissionLogEntry.created_at))
        .all()
    )
    return _log_entries


def update_mission_log_entry(_id: int, log_entry: str) -> None:
    """Update a mission log entry."""
    # session.begin()
    _log_entry = get_mission_log_entry_by_id(_id)
    if _log_entry:
        _log_entry.log_entry = log_entry
        session.commit()
