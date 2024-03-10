from textual import events
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

    def on_key(self, event: events.Key) -> None:
        if self.update_timer:
            self.update_timer.stop()
        self.app.switch_mode("home")

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(2, self.go_home, pause=False)

    def go_home(self) -> None:
        self.update_timer.stop()
        self.app.switch_mode("home")
