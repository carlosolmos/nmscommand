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
    TextArea,
)
from textual import events, on
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from model.dbmodels import Mission, MissionStage
from model.repository import create_mission_log_entry_simple
from nmswidgets.alertmessage import AlertModalScreen
from model.repository import get_mission_by_id


class NewMissionLog(Static):
    """
    New Mission Log Entry
    """

    mission_data: reactive[Mission | None] = reactive(None)
    log_entry: reactive[str | None] = reactive("")

    def __init__(self, _id: str, mission_id: str):
        super().__init__(id=_id)
        self.mission_id = mission_id
        self.mission_data = get_mission_by_id(mission_id)

    def compose(self) -> ComposeResult:
        with Vertical():
            with Vertical():
                yield Static(
                    f"Mission: {self.mission_data.codename}",
                    id="mission_name",
                    classes="",
                )
                yield TextArea.code_editor(
                    "",
                    language="markdown",
                    id="log_entry_text",
                    theme="vscode_dark",
                    classes="new_mission_input_text",
                )
                with Horizontal(classes="button_container"):
                    yield Button("Submit", id="submit", variant="primary")
                    yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        """Called when app starts."""
        # Give the input focus, so we can start typing straight away
        self.query_one("#log_entry_text", TextArea).focus()

    @on(Button.Pressed, "#cancel")
    def cancelNewMission(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, "#submit")
    def saveNewLogEntry(self) -> None:

        def check_error(btn: bool) -> None:
            pass

        def check_okay(btn: bool) -> None:
            if btn:
                self.app.uninstall_screen(AlertModalScreen)
                self.app.pop_screen()

        # process submit
        self.log_entry = self.query_one("#log_entry_text", TextArea).text
        try:
            if not self.log_entry:
                self.app.push_screen(
                    AlertModalScreen("alert_error", "Empty Log!"),
                    check_error,
                )
                return

            create_mission_log_entry_simple(self.mission_data.id, self.log_entry)

            self.app.push_screen(
                AlertModalScreen("alert_okay", "Log Recorded!"), check_okay
            )
            self.clearForm()
        except Exception as e:
            self.log(e)
            self.app.push_screen(
                AlertModalScreen("alert_error", f"Error: {e}"),
                check_error,
            )

    def clearForm(self) -> None:
        self.mission_name = ""
        self.log_entry = ""


class MissionLogScreen(Screen):
    """
    New Mission Log Entry Screen
    """

    BINDINGS = [("q", "quit", "Quit"), ("escape", "go_back", "Back")]
    TITLE = "New Log Entry"

    def __init__(
        self,
        _mission_id: str,
        _id: str,
    ):
        super().__init__(id=_id)
        self.mission_id = _mission_id

    def compose(self) -> ComposeResult:
        yield Header()
        yield NewMissionLog("new_log_form", self.mission_id)
        yield Footer()

    def action_go_back(self) -> None:
        self.app.pop_screen()
