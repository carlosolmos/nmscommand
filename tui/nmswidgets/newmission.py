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
from model.repository import create_mission
from nmswidgets.alertmessage import AlertModalScreen


NEW_MISION_TEMPLATE = """
> Mission Objectives...

"""


class NewMission(Static):
    """
    New Mission Package Form
    """

    mission_name: reactive[str | None] = reactive("")
    mission_description: reactive[str | None] = reactive("")
    start_date: reactive[str | None] = reactive("")
    mission_milestones: reactive[str | None] = reactive("")
    mission_swag: reactive[str | None] = reactive("")
    mission_resources: reactive[str | None] = reactive("")
    mission_tech: reactive[str | None] = reactive("")

    def __init__(self, _id: str):
        super().__init__(id=_id)

    def compose(self) -> ComposeResult:
        with Vertical():
            with Vertical():
                yield Input(
                    placeholder="CodeName",
                    id="mission_name",
                    classes="new_mission_input",
                )

                yield Input(
                    value=datetime.now().strftime("%Y-%m-%d"),
                    placeholder="Start Date: 0000-00-00",
                    id="start_date",
                    classes="new_mission_input_short",
                )

                yield TextArea.code_editor(
                    NEW_MISION_TEMPLATE,
                    language="markdown",
                    id="mission_description",
                    theme="vscode_dark",
                    classes="new_mission_input_text",
                )
                """
                yield Input(
                    placeholder="Objectives",
                    id="mission_description",
                    classes="new_mission_input",
                )
                yield Input(
                    placeholder="Milestones: m1,m2,m3",
                    id="mission_milestones",
                    classes="new_mission_input",
                )
                yield Input(
                    placeholder="Swag: s1,s2,s3",
                    id="mission_swag",
                    classes="new_mission_input",
                )
                yield Input(
                    placeholder="Resources: r1,r2,r3",
                    id="mission_resources",
                    classes="new_mission_input",
                )
                yield Input(
                    placeholder="Tech: t1,t2,t3",
                    id="mission_tech",
                    classes="new_mission_input",
                )
                """
                with Horizontal(classes="button_container"):
                    yield Button("Submit", id="submit", variant="primary")
                    yield Button("Cancel", id="cancel")

    def on_input_changed(self, event: Input.Changed) -> None:
        self.mission_name = self.query_one("#mission_name", Input).value
        self.mission_description = self.query_one("#mission_description", TextArea).text
        self.start_date = self.query_one("#start_date", Input).value
        # self.mission_milestones = self.query_one("#mission_milestones", Input).value
        # self.mission_swag = self.query_one("#mission_swag", Input).value
        # self.mission_resources = self.query_one("#mission_resources", Input).value
        # self.mission_tech = self.query_one("#mission_tech", Input).value

    def on_mount(self) -> None:
        """Called when app starts."""
        # Give the input focus, so we can start typing straight away
        self.query_one("#mission_name", Input).focus()

    @on(Button.Pressed, "#cancel")
    def cancelNewMission(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, "#submit")
    def saveNewMission(self) -> None:

        def check_error(btn: bool) -> None:
            pass

        def check_okay(btn: bool) -> None:
            if btn:
                self.app.uninstall_screen(AlertModalScreen)
                self.app.pop_screen()

        # process submit
        try:
            if not self.mission_name:
                self.app.push_screen(
                    AlertModalScreen("alert_error", "Mission Name is required!"),
                    check_error,
                )
                return

            if not self.start_date:
                _start_date = datetime.now()
            else:
                _start_date = datetime.strptime(self.start_date, "%Y-%m-%d")

            create_mission(
                codename=self.mission_name,
                description=self.query_one("#mission_description", TextArea).text,
                start_date=_start_date,
                end_date=_start_date,
                stage=MissionStage.Planning,
                milestones=(
                    self.mission_milestones.split(",") if self.mission_milestones else []
                ),
                swag=self.mission_swag.split(",") if self.mission_swag else [],
                tech=self.mission_tech.split(",") if self.mission_tech else [],
                resources=(
                    self.mission_resources.split(",") if self.mission_resources else []
                ),
                media=[],
            )
            self.app.push_screen(
                AlertModalScreen("alert_okay", "Mission Created!"), check_okay
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
        self.mission_description = ""
        self.start_date = (datetime.now().strftime("%Y-%m-%d"),)
        self.mission_milestones = ""
        self.mission_swag = ""
        self.mission_resources = ""
        self.mission_tech = ""


class NewMissionScreen(Screen):
    """
    New Mission Screen
    """

    BINDINGS = [("q", "quit", "Quit"), ("escape", "go_home", "Home")]
    TITLE = "New Mission Package"

    def compose(self) -> ComposeResult:
        yield Header()
        yield NewMission("new_mission_form")
        yield Footer()

    def action_go_home(self) -> None:
        self.app.pop_screen()
