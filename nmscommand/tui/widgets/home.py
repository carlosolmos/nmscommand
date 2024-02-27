"""
Home screen widget
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Footer, Header
from textual.containers import ScrollableContainer

from .dummydata import dummy_mission_log_entries, dummy_missions


class HomeWidget(Static):
    """
    Sample Widget
    """
    def __init__(self, _id: str, title: str = "The title"):
        super().__init__(id=_id)
        self.border_title = title
        self.border_subtitle = "Subtitle"

    def compose(self) -> ComposeResult:
        yield Static("Some", classes="home_widget_title")
        yield Static("Something")


class HomeLastActivity(Static):
    """
    Last activity from the log
    """
    def __init__(self, log_entries: list,  _id: str):
        super().__init__(id=_id)
        self.log_entries = log_entries
        self.border_title = "Last Activity"
        self.border_subtitle = "(l) log"

    def compose(self) -> ComposeResult:
        yield Static(f'[@click=\'app.bell\']{self.log_entries[0]["mission_name"][:20]}[/]', 
                     classes="home_box_link")
        yield Static(str(self.log_entries[0]["created_at"]), classes="home_box")
        yield Static(str(self.log_entries[0]["entry"]), classes="")


class HomeMissions(Static):
    """
    List of active missions
    """
    def __init__(self, missions: list,  _id: str):
        super().__init__(id=_id)
        self.missions = missions
        self.border_title = "Missions"
        self.border_subtitle = "(m) Mission Roster"

    def compose(self) -> ComposeResult:
        for mission in self.missions:
            yield Static(f'[@click=\'app.bell\']▫ {mission["name"][:20]}:[/] {mission["description"][:80]}',
                         classes="home_box_link")


class HomeArchive(Static):
    """
    List of catalogs
    """
    def __init__(self, _id: str):
        super().__init__(id=_id)
        self.border_title = "Archive"
        self.border_subtitle = "(a) Archive Files"

    def compose(self) -> ComposeResult:
        yield Static('[@click=\'app.bell\']▫ Systems >[/]', classes="home_box_link")
        yield Static('[@click=\'app.bell\']▫ Planets >[/]', classes="home_box_link")
        yield Static('[@click=\'app.bell\']▫ Bases >[/]', classes="home_box_link")
        yield Static('[@click=\'app.bell\']▫ Discoveries >[/]', classes="home_box_link")


class HomeSearch(Static):
    """
    Search box
    """
    def __init__(self, _id: str):
        super().__init__(id=_id)

    def compose(self) -> ComposeResult: 
        yield Static("[@click='app.bell']Search[/]")


class HomeScreen(Screen):
    """
    Home screen
    """
    BINDINGS = [("q", "quit", "Quit"),
                ("s", "app.bell", "Search")]
    TITLE = "NMS Command Home"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(
            HomeLastActivity( dummy_mission_log_entries, "last_activity"),
            HomeMissions(dummy_missions, "Missions"),
            HomeArchive("archive"),
            HomeSearch("search")
        )
