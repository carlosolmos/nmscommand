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
    mission_log_data: reactive[list[MissionLogEntry] | None] = reactive(None)

    def __init__(self, _id: str, mission_id: str | None):
        super().__init__(id=_id)
        self.mission_id = mission_id
        self.mission_data = get_mission_by_id(mission_id)
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

    def watch_mission_log_data(
        self, old_val: list[MissionLogEntry], new_val: list[MissionLogEntry]
    ) -> None:
        try:
            pass
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
        mission_log_table = self.query_one("#mission_log_table", DataTable)
        mission_log_table.add_columns("Date", "Description")
        if mission_log_table and self.mission_log_data:
            self.load_missions_data_rows(mission_log_table, self.mission_log_data)

    def on_data_table_row_selected(self, row: DataTable.RowSelected) -> None:
        print(row.row_key.value)

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
                id="mission_details_header",
            )
            yield VerticalScroll(
                Markdown(
                    self.mission_data.description,
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
        ("e", "edit", "Edit"),
        ("l", "new_log", "Log"),
        ("escape", "go_home", "Home"),
    ]
    TITLE = "New Mission Package"

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
            MissionDetailsScreen.mission_data, MissionDetailsScreen.mission_log_data
        )
        yield Footer()

    def action_go_home(self) -> None:
        self.app.pop_screen()

    def action_new_log(self) -> None:
        self.app.push_screen(MissionLogScreen(self.mission_id, "mission_log"))

    def on_screen_resume(self) -> None:
        self.mission_data = get_mission_by_id(self.mission_id)
        self.mission_log_data = get_all_mission_log_entries_by_mission_id(
            mission_id=self.mission_id
        )
