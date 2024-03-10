"""
Home screen widget
"""

from datetime import datetime
import asyncio
from textual.app import ComposeResult
from textual.events import Focus
from textual.screen import Screen
from textual.widgets import Static, Footer, Header, OptionList, Input, Label
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from .dummydata import dummy_mission_log_entries, dummy_missions

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
    active_message: reactive[str | None] = reactive("X")

    def __init__(self, missions: list, _id: str):
        super().__init__(id=_id)

        self.border_title = "Missions"
        self.border_subtitle = "(m) Mission Roster"

    def on_mount(self) -> None:
        self.lookup_active_missions()

    def compose(self) -> ComposeResult:
        yield Label(
            f"K={self.active_message} - {len(self.active_missions)}", id="mission_lbl"
        )
        yield OptionList(
            *[
                f"[@click='app.bell']▫ {mission.codename[:20]}:[/] {mission.description[:80]}"
                for mission in self.active_missions
            ],
            id="mission_list",
        )

    def watch_active_message(self, old_val: str, new_val: str) -> None:
        print(f"******************Active message changed from {old_val} to {new_val}")
        try:
            self.query_one("#mission_lbl", Label).update(new_val)
            self.query_one("#mission_list", OptionList).update(
                *[
                    f"[@click='app.bell']▫ {mission.codename[:20]}:[/] {mission.description[:80]}"
                    for mission in self.active_missions
                ]
            )
        except Exception as e:
            pass

    def lookup_active_missions(self):
        try:
            self.app.active_missions = get_missions_active(_session=None)
        except Exception as e:
            self.log(e)


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
        ("n", "switch_mode('newmission')", "New Mission"),
        ("a", "app.bell", "Archive"),
        ("s", "app.bell", "Search"),
        ("space", "greeting"),
    ]
    TITLE = "NMS Command Home"

    _message: reactive[str | None] = reactive("Y")
    _missions: reactive[list[Mission] | None] = reactive([])

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(
            HomeLastActivity(dummy_mission_log_entries, "last_activity"),
            HomeMissions(dummy_missions, "Missions").data_bind(
                active_message=HomeScreen._message, active_missions=HomeScreen._missions
            ),
            HomeArchive("archive"),
            HomeSearch("search"),
        )

    def on_mount(self) -> None:
        print("HomeScreen mounted")

    def on_screen_resume(self) -> None:
        print("=======================Resuming HomeScreen")
        self._missions = get_missions_active(_session=None)
        self._message = f"HOLAX {datetime.now().strftime("%H:%M:%S")} - {len(self._missions)}"
