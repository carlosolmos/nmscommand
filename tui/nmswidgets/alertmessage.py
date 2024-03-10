from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Vertical


class AlertModalScreen(ModalScreen[bool]):
    """Screen with a message."""

    def __init__(self, _id: str, message: str):
        super().__init__(id=_id)
        self.message = message

    def compose(self) -> ComposeResult:
        variant = "primary" if self._id == "alert_okay" else "error"

        yield Vertical(
            Label(self.message, id="alert_message"),
            Button("Okay", variant=variant, id="alert_message_okay"),
            id="alert_message_dialog",
        )

    def on_mount(self) -> None:
        self.focus("alert_message_okay")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(True)
