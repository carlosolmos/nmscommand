"""
Launcher for NMSCommand
"""
from textual.app import App
from nmscommand.tui.nmswidgets.welcome import NMSWelcomeScreen
from nmscommand.tui.nmswidgets.home import HomeScreen
from nmscommand.tui.nmswidgets.newmission import NewMissionScreen
from nmscommand.tui.nmswidgets.missiondetails import MissionDetailsScreen

class NMSCommandApp(App):
    """Textual app for NMSCommand."""

    CSS_PATH = "nmscommand.tcss"
    MODES = {"welcome": NMSWelcomeScreen()}
    BINDINGS = [("1", "switch_mode('welcome')", "Welcome"), 
                ("2", "switch_mode('home')", "Home"),
                ("3", "switch_mode('newmission')", "New Mission"),
                ("4", "switch_mode('missiondetails')", "New Mission"),
                ("q", "quit", "Quit")]

    MODES = {"welcome": NMSWelcomeScreen, 
             "home": HomeScreen,
             "newmission": NewMissionScreen,
             "missiondetails": MissionDetailsScreen}

    def on_mount(self) -> None:
        """Mount the welcome screen on startup."""
        self.switch_mode("welcome")

if __name__ == "__main__":
    app = NMSCommandApp()
    app.run()
