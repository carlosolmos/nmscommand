"""
Launcher for NMSCommand
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../tui"))

from textual.app import App
from nmswidgets.welcome import NMSWelcomeScreen
from nmswidgets.home import HomeScreen
from nmswidgets.newmission import NewMissionScreen
from nmswidgets.missiondetails import MissionDetailsScreen
import logging
from textual.logging import TextualHandler
from textual.reactive import reactive
from model.dbmodels import Mission, MissionStage

logging.basicConfig(
    level="INFO",
    handlers=[TextualHandler()],
)


class NMSCommandApp(App):
    """Textual app for NMSCommand."""

    CSS_PATH = "nmscommand.tcss"
    BINDINGS = [
        ("ctrl+h", "switch_mode('welcome')", "Welcome"),
        ("2", "switch_mode('home')", "Home"),
        ("m", "switch_mode('missiondetails')", "Mission"),
        ("ctrl+q", "quit", "Quit"),
    ]

    MODES = {
        "welcome": NMSWelcomeScreen,
        "home": HomeScreen,
        "missiondetails": MissionDetailsScreen,
    }

    def on_mount(self) -> None:
        """Mount the welcome screen on startup."""
        self.switch_mode("welcome")


if __name__ == "__main__":
    app = NMSCommandApp()
    app.run()
