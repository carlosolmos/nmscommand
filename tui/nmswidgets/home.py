"""
Home screen widget
"""

from datetime import datetime
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Static,
    Footer,
    Header,
    OptionList,
    Input,
    DataTable,
)
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from .dummydata import dummy_mission_log_entries, dummy_missions
from nmswidgets.newmission import NewMissionScreen
from nmswidgets.missiondetails import MissionDetailsScreen
from model.repository import get_missions_active, get_last_mission_log_entry
from model.dbmodels import (
    Mission,
    MissionLogEntry,
    get_mission_stage_string,
)


class HomeLastActivity(Static):
    """
    Last activity from the log
    """

    last_activity: reactive[MissionLogEntry | None] = reactive(None)

    mission_name: reactive[str | None] = reactive("")
    entry_date: reactive[str | None] = reactive("")
    log_entry: reactive[str | None] = reactive("")

    def __init__(self, log_entries: list, _id: str):
        super().__init__(id=_id)
        self.last_activity = get_last_mission_log_entry()
        if self.last_activity is not None:
            self.mission_name = self.last_activity.mission.codename[:25]
            self.entry_date = self.last_activity.created_at.strftime("%Y-%m-%d %H:%M")
            self.log_entry = self.last_activity.log_entry[:160]
        self.border_title = "Last Activity"
        self.border_subtitle = "(l) Log"

    def compose(self) -> ComposeResult:
        yield Static(
            f"[@click='app.bell']{self.mission_name}[/]",
            classes="home_box_link",
        )
        yield Static(
            self.entry_date,
            classes="home_box",
        )
        yield Static(self.log_entry, classes="")

    def watch_last_activity(
        self, old_val: MissionLogEntry, new_val: MissionLogEntry
    ) -> None:
        if new_val is not None:
            self.mission_name = new_val.mission.codename[:25]
            self.entry_date = new_val.created_at.strftime("%Y-%m-%d %H:%M")
            self.log_entry = new_val.log_entry[:160]


class HomeMissions(Static):
    """
    List of active missions
    """

    active_missions: reactive[list[Mission] | None] = reactive([])

    def __init__(self, missions: list, _id: str):
        super().__init__(id=_id)

        self.border_title = "Missions"
        self.border_subtitle = "(m) Mission Roster"

        ROWS = []

    def on_mount(self) -> None:
        self.lookup_active_missions()
        table = self.query_one(DataTable)
        table.add_columns("Mission", "Stage", "Started", "Description")
        self.load_missions_data_rows(table, self.active_missions)

    def compose(self) -> ComposeResult:
        yield DataTable(
            show_header=False,
            show_row_labels=False,
            id="mission_table",
            classes="missions_data_table",
            cursor_type="row",
        )

    def watch_active_missions(
        self, old_val: list[Mission], new_val: list[Mission]
    ) -> None:
        try:
            table = self.query_one(DataTable)
            self.load_missions_data_rows(table, new_val)
            self.query_one("#mission_table", DataTable).focus()
        except Exception as e:
            self.log(e)
            pass

    def lookup_active_missions(self):
        try:
            self.app.active_missions = get_missions_active()
        except Exception as e:
            self.log(e)

    def load_missions_data_rows(
        self, table: DataTable, active_missions: list[Mission]
    ) -> list:
        table.clear()
        for mission in active_missions:
            table.add_row(
                mission.codename[:20],
                get_mission_stage_string(mission.stage),
                mission.start_date.strftime("%Y-%m-%d"),
                mission.description[:80],
                key=mission.id,
            )
        return table

    def on_data_table_row_selected(self, row: DataTable.RowSelected) -> None:
        self.app.push_screen(MissionDetailsScreen(row.row_key.value, "mission_details"))


class HomeArchive(Static):
    """
    List of catalogs
    """

    def __init__(self, _id: str):
        super().__init__(id=_id)
        self.border_title = "Archive"
        self.border_subtitle = "(a) Archive Files"

    def compose(self) -> ComposeResult:
        yield OptionList("▫ Systems >", "▫ Planets >", "▫ Bases >", "▫ Discoveries >")


class HomeSearch(Static):
    """
    Search box
    """

    def __init__(self, _id: str):
        super().__init__(id=_id)
        self.border_subtitle = "(s) Advanced Search"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search", id="search", classes="home_search")


class HomeScreen(Screen):
    """
    Home screen
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("l", "app.bell", "Log"),
        ("m", "app.bell", "Missions"),
        ("n", "new_mission", "New Mission"),
        ("a", "app.bell", "Archive"),
        ("s", "app.bell", "Search"),
        ("space", "greeting"),
    ]
    TITLE = "NMS Command Home"

    active_missions: reactive[list[Mission] | None] = reactive([])
    last_activity: reactive[MissionLogEntry | None] = reactive(None)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(
            HomeLastActivity(dummy_mission_log_entries, "last_activity").data_bind(
                HomeScreen.last_activity
            ),
            HomeMissions(dummy_missions, "Missions").data_bind(
                HomeScreen.active_missions
            ),
            HomeArchive("archive"),
            HomeSearch("search"),
        )

    def on_mount(self) -> None:
        try:
            self.query_one("#mission_table", DataTable).focus()
        except Exception as e:
            pass

    def on_screen_resume(self) -> None:
        self.log("Resuming Home Screen")
        self.active_missions = get_missions_active()
        self.last_activity = get_last_mission_log_entry()

    def action_new_mission(self) -> None:
        self.app.push_screen(NewMissionScreen("newmission"))
