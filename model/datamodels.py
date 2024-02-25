"""
from typing import List, Union
from datetime import datetime
from enum import Enum

class MissionStage(Enum):
    Planning = 0
    Sourcing = 1
    InProgress = 2
    Complete = 3
    Aborted = 4

class AssetClass(Enum):
    C = 0
    B = 1
    A = 2
    S = 3

class StarColor(Enum):
    Yellow = 0
    Red = 1
    Blue = 2
    Green = 3

class ListItem:
    def __init__(self, description: str, completed: bool):
        self.description = description
        self.completed = completed

class DBBaseModel:
    def __init__(self):
        self.ID: str = None
        self.CreatedAt: datetime = None
        self.UpdatedAt: datetime = None
        self.DeletedAt: Union[datetime, None] = None

class MissionLogEntry(DBBaseModel):
    def __init__(self):
        super().__init__()
        self.MissionID: str = None
        self.Entry: str = None
        self.SystemID: Union[str, None] = None
        self.PlanetID: Union[str, None] = None
        self.BaseID: Union[str, None] = None
        self.Media: List[str] = []

class Discovery(DBBaseModel):
    def __init__(self):
        super().__init__()
        self.MissionID: Union[str, None] = None
        self.SystemID: Union[str, None] = None
        self.PlanetID: Union[str, None] = None
        self.Description: str = None
        self.Wonder: bool = False
        self.Media: List[str] = []

class Base(DBBaseModel):
    def __init__(self):
        super().__init__()
        self.PlanetID: str = None
        self.BaseName: str = None
        self.BaseType: Union[str, None] = None
        self.Description: Union[str, None] = None
        self.Ammenities: List[str] = []
        self.Resources: List[str] = []
        self.Media: List[str] = []

class Mission(DBBaseModel):
    def __init__(self):
        super().__init__()
        self.Codename: str = None
        self.Description: Union[str, None] = None
        self.StartDate: Union[datetime, None] = None
        self.EndDate: Union[datetime, None] = None
        self.Stage: MissionStage = MissionStage.Planning
        self.Milestones: List[ListItem] = []
        self.Swag: List[ListItem] = []
        self.Tech: List[ListItem] = []
        self.Resources: List[ListItem] = []
        self.Log: List[MissionLogEntry] = []
        self.Media: List[str] = []

class System(DBBaseModel):
    def __init__(self):
        super().__init__()
        self.Galaxy: str = None
        self.Region: Union[str, None] = None
        self.System: Union[str, None] = None
        self.Civilization: Union[str, None] = None
        self.StarColor: Union[StarColor, None] = None
        self.BlackHole: bool = False
        self.Atlas: bool = False
        self.Outlaw: bool = False

class Planet(DBBaseModel):
    def __init__(self):
        super().__init__()
        self.SystemID: str = None
        self.Name: str = None
        self.Type: Union[str, None] = None
        self.Alias: Union[str, None] = None
        self.PortalCoords: List[int] = []
        self.Resources: List[str] = []
        self.Ecosystem: List[str] = []
        self.Description: str = None
        self.Dissonant: bool = False
        self.Media: List[str] = []
"""