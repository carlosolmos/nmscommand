"""
Home screen widget
"""

from datetime import datetime
import asyncio
from textual.app import ComposeResult
from textual.events import Focus
from textual.screen import Screen
from textual.widgets import Static, Footer, Header, OptionList, Input, Label, DataTable
from textual.widgets.option_list import Option, Separator
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from .dummydata import dummy_mission_log_entries, dummy_missions
from nmswidgets.newmission import NewMissionScreen
from model.repository import get_missions_active
from model.dbmodels import Mission


class HomeLastActivity(Static):
    """
    Last activity from the log
    """

    def __init__(self, log_entries: list, _id: str):
        super().__init__(id=_id)
        self.log_entries = log_entries
        self.border_title = "Last Activity"
        self.border_subtitle = "(l) Log"

    def compose(self) -> ComposeResult:
        yield Static(
            f'[@click=\'app.bell\']{self.log_entries[0]["mission_name"][:20]}[/]',
            classes="home_box_link",
        )
        yield Static(str(self.log_entries[0]["created_at"]), classes="home_box")
        yield Static(str(self.log_entries[0]["entry"]), classes="")


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
        for mission in self.active_missions:
            table.add_row(
                mission.codename[:20],
                mission.stage,
                mission.start_date.strftime("%Y-%m-%d"),
                mission.description[:60],
            )

    def compose(self) -> ComposeResult:
        yield DataTable(show_header=False, show_row_labels=False, id="mission_table")

    def watch_active_missions(
        self, old_val: list[Mission], new_val: list[Mission]
    ) -> None:
        try:
            table = self.query_one(DataTable)
            table.clear()
            table.add_rows(self.load_missions_data_rows(new_val))

        except Exception as e:
            self.log(e)
            pass

    def lookup_active_missions(self):
        try:
            self.app.active_missions = get_missions_active(_session=None)
        except Exception as e:
            self.log(e)

    def load_missions_data_rows(self, active_missions) -> list:
        rows = []
        for mission in active_missions:
            rows.append(
                (
                    mission.codename[:20],
                    mission.stage,
                    mission.start_date.strftime("%Y-%m-%d"),
                    mission.description[:80],
                )
            )
        return rows


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

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(
            HomeLastActivity(dummy_mission_log_entries, "last_activity"),
            HomeMissions(dummy_missions, "Missions").data_bind(
                HomeScreen.active_missions
            ),
            HomeArchive("archive"),
            HomeSearch("search"),
        )

    def on_mount(self) -> None:
        pass

    def on_screen_resume(self) -> None:
        self.log("Resuming Home Screen")
        self.active_missions = get_missions_active(_session=None)

    def action_new_mission(self) -> None:
        self.app.push_screen(NewMissionScreen("newmission"))
