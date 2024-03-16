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
    DataTable,
)
from rich.syntax import Syntax
from textual.containers import Vertical, VerticalScroll, Horizontal
from textual.reactive import reactive
from model.repository import get_mission_by_id, get_all_mission_log_entries_by_mission_id
from model.dbmodels import Mission, CheckListItem, MissionLogEntry
from nmswidgets.newmissionlog import MissionLogScreen
from nmswidgets.detailsmissionlog import MissionLogDetailsScreen
from nmswidgets.editmission import EditMissionScreen

"""
class MissionPackageList(Static):
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
"""


class MissionDetails(Static):
    """
    Mission Package
    """

    dirty: reactive[bool] = reactive(False)
    mission_data: reactive[Mission | None] = reactive(None)
    mission_log_data: reactive[list[MissionLogEntry] | None] = reactive(None)
    mission_codename: reactive[str | None] = reactive("")
    mission_description: reactive[str | None] = reactive("")
    mission_start_date: reactive[str | None] = reactive("")

    def __init__(self, _id: str, mission_id: str | None):
        super().__init__(id=_id)
        self.mission_id = mission_id
        self.mission_data = get_mission_by_id(mission_id)
        self.mission_codename = self.mission_data.codename
        self.mission_description = self.mission_data.description
        self.mission_start_date = self.mission_data.start_date.strftime("%Y-%m-%d")
        self.mission_log_data = get_all_mission_log_entries_by_mission_id(
            mission_id=mission_id
        )
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

    def wath_dirty(self, old_val: bool, new_val: bool) -> None:
        print("************************* watch_dirty")
        self.dirty = False

    def watch_mission_log_data(
        self, old_val: list[MissionLogEntry], new_val: list[MissionLogEntry]
    ) -> None:
        print("************************* watch_mission_log_data")
        try:
            mission_log_table = self.query_one("#mission_log_table", DataTable)
            if mission_log_table:
                mission_log_table.clear()
                self.load_missions_data_rows(mission_log_table, new_val)
        except Exception as e:
            self.log(e)
            pass

    def watch_mission_data(self, old_val: Mission, new_val: Mission) -> None:
        try:
            print("************************* watch_mission_data")
            self.mission_codename = new_val.codename
            self.mission_description = new_val.description
            self.mission_start_date = new_val.start_date.strftime("%Y-%m-%d")
            mission_name = self.query_one("#mission_name", Static)
            if mission_name:
                mission_name.text = new_val.codename
            mission_description = self.query_one("#mission_description", Markdown)
            if mission_description:
                mission_description.text = new_val.description
            mission_start_date = self.query_one("#start_date", Static)
            if mission_start_date:
                mission_start_date.text = new_val.start_date.strftime("%Y-%m-%d")
        except Exception as e:
            self.log(e)
            pass

    def load_missions_data_rows(
        self, table: DataTable, mission_log: list[MissionLogEntry]
    ) -> list:
        table.clear()
        if mission_log:
            for entry in mission_log:
                table.add_row(
                    entry.created_at.strftime("%Y-%m-%d %H:%M"),
                    entry.log_entry[:120],
                    key=entry.id,
                )
        return table

    def on_mount(self) -> None:
        print("-------------------------- on_mount MissionDetails")
        mission_log_table = self.query_one("#mission_log_table", DataTable)
        mission_log_table.add_columns("Date", "Description")
        if mission_log_table and self.mission_log_data:
            self.load_missions_data_rows(mission_log_table, self.mission_log_data)

    def on_data_table_row_selected(self, row: DataTable.RowSelected) -> None:
        self.app.push_screen(
            MissionLogDetailsScreen(
                self.mission_id, row.row_key.value, "mission_log_details"
            )
        )

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Horizontal(
                Static("CodeName: ", classes="mission_details_label"),
                Static(
                    self.mission_codename,
                    id="mission_name",
                    classes="mission_details_value",
                ),
                Static("Start Date: ", classes="mission_details_label"),
                Static(
                    self.mission_start_date,
                    id="start_date",
                    classes="mission_details_value",
                ),
                classes="mission_details_row",
                id="mission_details_header",
            )
            yield VerticalScroll(
                Markdown(
                    self.mission_description,
                    id="mission_description",
                    classes="mission_description_rich",
                ),
                DataTable(
                    show_header=False,
                    show_row_labels=False,
                    id="mission_log_table",
                    classes="missions_log_table",
                    cursor_type="row",
                ),
                id="mission_description_container_top",
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
        ("e", "edit_mission", "Edit"),
        ("l", "new_log", "Log"),
        ("escape", "go_home", "Home"),
    ]
    TITLE = "New Mission Package"

    dirty: reactive[bool] = reactive(False)
    mission_data: reactive[Mission | None] = reactive(None)
    mission_log_data: reactive[list[MissionLogEntry] | None] = reactive(None)

    def __init__(
        self,
        _mission_id: str,
        _id: str,
    ):
        super().__init__(id=_id)
        self.mission_id = _mission_id

    def compose(self) -> ComposeResult:
        yield Header()
        yield MissionDetails("mission_details_view", self.mission_id).data_bind(
            mission_data=MissionDetailsScreen.mission_data,
            mission_log_data=MissionDetailsScreen.mission_log_data,
            dirty=MissionDetailsScreen.dirty,
        )
        yield Footer()

    def action_go_home(self) -> None:
        self.app.pop_screen()

    def action_new_log(self) -> None:
        self.app.push_screen(MissionLogScreen(self.mission_id, "mission_log"))

    def action_edit_mission(self) -> None:
        self.app.push_screen(EditMissionScreen(self.mission_id, "mission_edit"))

    def on_screen_resume(self) -> None:
        self.dirty = True
        self.mission_data = get_mission_by_id(self.mission_id)
        self.mission_log_data = get_all_mission_log_entries_by_mission_id(
            mission_id=self.mission_id
        )
