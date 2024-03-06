"""
Home screen widget
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Footer, Header, OptionList, Input
from textual.containers import ScrollableContainer

from .dummydata import dummy_mission_log_entries, dummy_missions


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

    def __init__(self, missions: list, _id: str):
        super().__init__(id=_id)
        self.missions = missions
        self.border_title = "Missions"
        self.border_subtitle = "(m) Mission Roster"

    def compose(self) -> ComposeResult:
        yield OptionList(
            *[
                f'[@click=\'app.bell\']▫ {mission["name"][:20]}:[/] {mission["description"][:80]}'
                for mission in self.missions
            ]
        )


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
        ("a", "app.bell", "Archive"),
        ("s", "app.bell", "Search"),
    ]
    TITLE = "NMS Command Home"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(
            HomeLastActivity(dummy_mission_log_entries, "last_activity"),
            HomeMissions(dummy_missions, "Missions"),
            HomeArchive("archive"),
            HomeSearch("search"),
        )
