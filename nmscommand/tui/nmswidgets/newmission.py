""" New Mission Widget """

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Footer,
    Header,
    Input,
    Button,
    Static,
)
from textual.containers import Vertical, Horizontal


class NewMission(Static):
    """
    New Mission Package Form
    """

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
                    placeholder="Objectives",
                    id="mission_description",
                    classes="new_mission_input",
                )
                yield Input(
                    placeholder="Start Date: 0000-00-00",
                    id="start_date",
                    classes="new_mission_input_short",
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

                with Horizontal(classes="button_container"):
                    yield Button("Submit", id="submit", variant="primary")
                    yield Button("Cancel", id="cancel")


class NewMissionScreen(Screen):
    """
    New Mission Screen
    """

    BINDINGS = [("q", "quit", "Quit"), ("H", "switch_mode('home')", "Home")]
    TITLE = "New Mission Package"

    def compose(self) -> ComposeResult:
        yield Header()
        yield NewMission("new_mission_form")
        yield Footer()
