""" New Mission Widget """

import os
import sys
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Footer,
    Header,
    Input,
    Button,
    Static,
    Markdown,
)
from textual import events, on
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from model.dbmodels import Mission, MissionStage, MissionLogEntry
from model.repository import create_mission_log_entry_simple
from nmswidgets.alertmessage import AlertModalScreen
from model.repository import get_mission_by_id, get_mission_log_entry_by_id


class MissionLog(Static):
    """
    Mission Log Entry
    """

    mission_data: reactive[Mission | None] = reactive(None)
    log_entry_data: reactive[MissionLogEntry | None] = reactive("")

    def __init__(self, _id: str, mission_id: str, log_id: str):
        super().__init__(id=_id)
        self.mission_id = mission_id
        self.mission_data = get_mission_by_id(mission_id)
        self.log_entry_data = get_mission_log_entry_by_id(log_id)

    def compose(self) -> ComposeResult:
        with Vertical():
            with Vertical():
                yield Static(
                    f"Mission: {self.mission_data.codename}",
                    id="mission_name",
                    classes="field_label",
                )
                yield Static(
                    f"Date: {self.log_entry_data.created_at.strftime('%Y-%m-%d %H:%M')}",
                    id="entry_date",
                    classes="field_label",
                )
                yield Markdown(
                    self.log_entry_data.log_entry,
                    id="log_entry_text",
                    classes="mission_description_rich",
                )

    def on_mount(self) -> None:
        """Called when app starts."""
        # Give the input focus, so we can start typing straight away
        self.query_one("#log_entry_text", Markdown).focus()

    @on(Button.Pressed, "#cancel")
    def cancelNewMission(self) -> None:
        self.app.pop_screen()

    def clearForm(self) -> None:
        self.mission_name = ""
        self.log_entry = ""


class MissionLogDetailsScreen(Screen):
    """
    Mission Log Entry Screen
    """

    BINDINGS = [("q", "quit", "Quit"), ("escape", "go_back", "Back")]
    TITLE = "Log Entry"

    def __init__(
        self,
        _mission_id: str,
        _log_id: str,
        _id: str,
    ):
        super().__init__(id=_id)
        self.mission_id = _mission_id
        self.log_id = _log_id

    def compose(self) -> ComposeResult:
        yield Header()
        yield MissionLog("log_detail", self.mission_id, self.log_id)
        yield Footer()

    def action_go_back(self) -> None:
        self.app.pop_screen()
