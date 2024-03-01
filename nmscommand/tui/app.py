"""
Launcher for NMSCommand
"""
from textual.app import App
# import NMSWelcome from widgets/welcome
from widgets.welcome import NMSWelcomeScreen
from widgets.home import HomeScreen


class NMSCommandApp(App):
    """Textual app for NMSCommand."""

    CSS_PATH = "nmscommand.tcss"
    MODES = {"welcome": NMSWelcomeScreen()}
    BINDINGS = [("1", "switch_mode('welcome')", "Welcome"), 
                ("2", "switch_mode('home')", "Home"),
                ("q", "quit", "Quit")]

    MODES = {"welcome": NMSWelcomeScreen, 
             "home": HomeScreen}

    def on_mount(self) -> None:
        """Mount the welcome screen on startup."""
        self.switch_mode("welcome")

if __name__ == "__main__":
    app = NMSCommandApp()
    app.run()
