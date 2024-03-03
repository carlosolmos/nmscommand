""" New Mission Widget """

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Footer, 
    Header, 
    Input, 
    Button, 
    TabbedContent, 
    TabPane,
    Static, 
    OptionList
)
from textual.containers import Vertical, Horizontal, ScrollableContainer, VerticalScroll


class MilestonesList(Static):
    """
    List of Milestones
    """
    def __init__(self, _id: str):
        super().__init__(id=_id)
        self.border_subtitle = "(a) add milestone"

    def compose(self) -> ComposeResult:
        yield OptionList(
            "▫ Milestone 1",
            "▫ Milestone 2",
            "▫ Milestone 3",
            "▫ Milestone 4",
            "▫ Milestone 5",
            "▫ Milestone 6",
            "▫ Milestone 7",
        )



class NewMission(Static):
    """
    New Mission Package Form
    """
    def __init__(self, _id: str):
        super().__init__(id=_id)

    def compose(self) -> ComposeResult:
        with Vertical():
            with Vertical():
                yield Input(placeholder="CodeName", id="mission_name", classes="new_mission_input")
                yield Input(placeholder="Objectives", id="mission_description", classes="new_mission_input")
                yield Input(placeholder="Start Date: 0000-00-00", id="start_date", classes="new_mission_input_short") 
                with TabbedContent():
                    with TabPane("Milestones", id="nm_milestones"):
                        yield MilestonesList("nm_milestones_list")
                    with TabPane("Swag", id="nm_swag"):
                        yield Static("Swag", id="swag")
                    with TabPane("Resources", id="nm_resources"):
                        yield Static("Resources", id="resources")
                    with TabPane("Tech", id="nm_tech"):
                        yield Static("Tech", id="tech")

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