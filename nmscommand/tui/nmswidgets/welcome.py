from textual.app import ComposeResult
from textual.widgets import Static
from textual.screen import Screen
from textual.containers import Container


WELCOME_MESSAGE = """
Welcome to NMSCommand!

Don't Panic!
"""


class NMSWelcomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Static(WELCOME_MESSAGE, classes="welcome_message"),
            id="welcome_container",
        )
