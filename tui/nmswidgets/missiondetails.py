"""  Mission Widget """

import jsons
from textual.app import ComposeResult
from textual.events import Mount
from textual.screen import Screen
from textual.widgets import (
    Footer,
    Header,
    Label,
    TabbedContent,
    TabPane,
    Static,
    Checkbox,
    Markdown,
)
from rich.syntax import Syntax
from textual.containers import Vertical, VerticalScroll, Horizontal
from textual.reactive import reactive
from model.repository import get_mission_by_id
from model.dbmodels import Mission, CheckListItem


class MissionPackageList(Static):
    """
    List of Milestones
    """

    data: reactive[str | None] = reactive("")

    def __init__(
        self,
        _id: str,
        name: str,
        data: list[CheckListItem],
        mark: str = "☐",
    ):
        super().__init__(id=_id)
        self.border_title = name
        self.data = data
        self.mark = mark

    def compose(self) -> ComposeResult:
        int_id = 0
        with VerticalScroll():
            for item in self.data:
                int_id += 1
                chk_id = f"{self.id}_{int_id}"
                yield Checkbox(f"{self.mark} {item.description}", item.checked, id=chk_id)


TEXT = """
> Log entry 1, 2021-10-10, 12:00, Mission 1, Stage 1, this is a log entry
 """


class MissionDetails(Static):
    """
    Mission Package
    """

    mission_data: reactive[Mission | None] = reactive(None)

    def __init__(self, _id: str, mission_id: str | None):
        super().__init__(id=_id)
        self.mission_id = mission_id
        self.mission_data = get_mission_by_id(mission_id)
        # load the milestos dictionary into list of CheckListItem
        self.milestones = [
            CheckListItem(item["description"], item["checked"])
            for item in self.mission_data.milestones
        ]
        self.swag = [
            CheckListItem(item["description"], item["checked"])
            for item in self.mission_data.swag
        ]
        self.tech = [
            CheckListItem(item["description"], item["checked"])
            for item in self.mission_data.tech
        ]
        self.resources = [
            CheckListItem(item["description"], item["checked"])
            for item in self.mission_data.resources
        ]

    def on_mount(self) -> None:
        pass

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Horizontal(
                Static("CodeName: ", classes="mission_details_label"),
                Static(
                    self.mission_data.codename,
                    id="mission_name",
                    classes="mission_details_value",
                ),
                Static("Start Date: ", classes="mission_details_label"),
                Static(
                    self.mission_data.start_date.strftime("%Y-%m-%d"),
                    id="start_date",
                    classes="mission_details_value",
                ),
                classes="mission_details_row",
            )
            yield VerticalScroll(
                Markdown(
                    self.mission_data.description,
                    id="mission_description",
                    classes="mission_description_rich",
                ),
                id="mission_description_container_top",
                classes="mission_description_container",
            )
            yield VerticalScroll(
                Markdown(
                    TEXT,
                    id="mission_log",
                    classes="mission_log_rich",
                ),
                id="mission_description_container_bottom",
                classes="mission_description_container",
            )

            # with TabbedContent():
            #     with TabPane("Milestones", id="nm_milestones"):
            #         yield MissionPackageList(
            #             data=self.milestones,
            #             _id="milestones",
            #             name="Milestones",
            #         )
            #     with TabPane("Swag", id="nm_swag"):
            #         yield MissionPackageList(
            #             data=self.swag,
            #             _id="swag",
            #             name="Swag",
            #         )
            #     with TabPane("Resources", id="nm_resources"):
            #         yield MissionPackageList(
            #             data=self.resources,
            #             _id="resources",
            #             name="Resources",
            #         )
            #     with TabPane("Tech", id="nm_tech"):
            #         yield MissionPackageList(
            #             data=self.tech,
            #             _id="tech",
            #             name="Technology",
            #         )


class MissionDetailsScreen(Screen):
    """
    Mission Screen
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("e", "edit", "Edit"),
        ("escape", "go_home", "Home"),
    ]
    TITLE = "New Mission Package"

    def __init__(
        self,
        _mission_id: str,
        _id: str,
    ):
        super().__init__(id=_id)
        self.mission_id = _mission_id

    def compose(self) -> ComposeResult:
        yield Header()
        yield MissionDetails("mission_details_view", self.mission_id)
        yield Footer()

    def action_go_home(self) -> None:
        self.app.pop_screen()
