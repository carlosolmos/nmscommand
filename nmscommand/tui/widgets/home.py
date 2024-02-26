"""
Home screen
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Footer, Header, Label
from textual.containers import ScrollableContainer
from textual import log

from .dummydata import dummy_mission_log_entries

class HomeWidget(Static):
    def __init__(self, title: str = "The title"):
        super().__init__()
        self.border_title = title
        self.border_subtitle = "Subtitle"

    def compose(self) -> ComposeResult:
        yield Static("Some", classes="home_widget_title")
        yield Static("Something")
        


class HomeLastActivity(Static):
    def __init__(self, log_entries: list):
        super().__init__()
        self.log_entries = log_entries
        self.border_title = "Last Activity"
        self.border_subtitle = "(l) log"
        

    def compose(self) -> ComposeResult:
        yield Static(str(self.log_entries[0]["created_at"]), classes="home_box")
        yield Static(str(self.log_entries[0]["entry"][:52]), classes="")



class HomeSearch(Static):
    def compose(self) -> ComposeResult: 
        yield Static("[@click='app.bell']Search[/]")


class HomeScreen(Screen):
    BINDINGS = [("q", "quit", "Quit"), 
                ("s", "app.bell", "Search")]
    TITLE = "NMS Command Home"

    def compose(self) -> ComposeResult:
        yield Header() 
        yield Footer()
        yield ScrollableContainer(
            HomeLastActivity(dummy_mission_log_entries),
            HomeWidget("Missions"),
            HomeWidget("Archive"),
            HomeSearch()
        
        )
       