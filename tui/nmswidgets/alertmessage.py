from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Grid


class AlertModalScreen(ModalScreen[bool]):
    """Screen with a message."""

    def __init__(self, _id: str, message: str):
        super().__init__(id=_id)
        self.message = message

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.message, id="alert_message"),
            Button("Okay", variant="primary", id="okay"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(True)
