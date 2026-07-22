"""
PyChronicle - Terminal UI Scaffolding (Week 2)

Initializes the Textual App shell: a code-view pane on the left and a
timeline-scrubber pane on the right. Per the Week 3 plan, this scaffold
is not yet wired to the SQLite history -- that's where the timeline
slider will start actually highlighting historical lines of code.
"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static


class PyChronicleApp(App):
    """Week 2 scaffold: layout only. DB <-> timeline wiring arrives in Week 3."""

    CSS = """
    #main { height: 1fr; }
    #code-pane {
        width: 2fr;
        border: solid green;
        padding: 1;
    }
    #timeline-pane {
        width: 1fr;
        border: solid cyan;
        padding: 1;
    }
    #timeline-position {
        content-align: center middle;
        height: 3;
        border: round white;
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("left", "scrub_back", "Scrub Back"),
        ("right", "scrub_forward", "Scrub Forward"),
    ]

    current_step = 0

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main"):
            yield Static(
                "Code view will render the traced script here.\n"
                "(Line highlighting arrives in Week 3)",
                id="code-pane",
            )
            with Vertical(id="timeline-pane"):
                yield Static("Timeline Scrubber")
                yield Static(f"Step: {self.current_step}", id="timeline-position")
                yield Static("Use \u2190 / \u2192 to scrub\n(wired to DB in Week 3)")
        yield Footer()

    def action_scrub_back(self) -> None:
        self.current_step = max(0, self.current_step - 1)
        self.query_one("#timeline-position", Static).update(f"Step: {self.current_step}")

    def action_scrub_forward(self) -> None:
        self.current_step += 1
        self.query_one("#timeline-position", Static).update(f"Step: {self.current_step}")


if __name__ == "__main__":
    PyChronicleApp().run()
