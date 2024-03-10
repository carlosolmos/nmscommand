import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)


import uuid
from datetime import timezone, datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, DeclarativeBase


def generate_uuid():
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class MissionStage:
    Planning = 0
    Sourcing = 1
    InProgress = 2
    Complete = 3
    Aborted = 4


class AssetClass:
    C = 0
    B = 1
    A = 2
    S = 3


class StarColor:
    Yellow = 0
    Red = 1
    Blue = 2
    Green = 3


class Mission(Base):
    __tablename__ = "missions"

    id = Column(String, primary_key=True, default=generate_uuid)
    codename = Column(String, unique=True)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    stage = Column(Integer, default=MissionStage.Planning)
    milestones = Column(JSON)
    swag = Column(JSON)
    tech = Column(JSON)
    resources = Column(JSON)
    log = relationship("MissionLogEntry", back_populates="mission")
    media = Column(JSON)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class System(Base):
    __tablename__ = "systems"

    id = Column(String, primary_key=True, default=generate_uuid)
    galaxy = Column(String)
    region = Column(String, nullable=True)
    system = Column(String, nullable=True)
    civilization = Column(String, nullable=True)
    star_color = Column(Integer, nullable=True)
    black_hole = Column(Boolean)
    atlas = Column(Boolean)
    outlaw = Column(Boolean)
    planets = relationship("Planet", back_populates="system")
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class Planet(Base):
    __tablename__ = "planets"

    id = Column(String, primary_key=True, default=generate_uuid)
    system_id = Column(String, ForeignKey("systems.id"))
    name = Column(String)
    type = Column(String, nullable=True)
    alias = Column(String, nullable=True)
    portal_coords = Column(JSON)
    resources = Column(JSON)
    ecosystem = Column(JSON)
    description = Column(String)
    dissonant = Column(Boolean)
    media = Column(JSON)
    system = relationship("System", back_populates="planets")
    planetbases = relationship("PlanetBase", back_populates="planet")
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class MissionLogEntry(Base):
    __tablename__ = "mission_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    mission_id = Column(String, ForeignKey("missions.id"))
    entry = Column(String)
    system_id = Column(String, ForeignKey("systems.id"), nullable=True)
    planet_id = Column(String, ForeignKey("planets.id"), nullable=True)
    planetbase_id = Column(String, ForeignKey("planetbases.id"), nullable=True)
    media = Column(JSON)
    mission = relationship("Mission", back_populates="log")
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class Discovery(Base):
    __tablename__ = "discoveries"

    id = Column(String, primary_key=True, default=generate_uuid)
    mission_id = Column(String, ForeignKey("missions.id"), nullable=True)
    system_id = Column(String, ForeignKey("systems.id"), nullable=True)
    planet_id = Column(String, ForeignKey("planets.id"), nullable=True)
    description = Column(String)
    wonder = Column(Boolean)
    media = Column(JSON)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class PlanetBase(Base):
    __tablename__ = "planetbases"

    id = Column(String, primary_key=True, default=generate_uuid)
    planet_id = Column(String, ForeignKey("planets.id"))
    base_name = Column(String)
    base_type = Column(String, nullable=True)
    description = Column(String, nullable=True)
    amenities = Column(JSON)
    resources = Column(JSON)
    media = Column(JSON)
    planet = relationship("Planet", back_populates="planetbases")
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
