"""Pop-up dialogs used throughout the app"""

from . import bindings

from textual.screen     import ModalScreen
from textual.widgets    import Button
from textual.widgets    import Label
from textual.containers import VerticalGroup
from textual.containers import HorizontalGroup
from textual.app        import ComposeResult

from collections.abc import Sequence
from typing          import Any


class ClickResponse(ModalScreen[str]):
    """Dialog asking the user to click a button to respond."""

    BINDINGS = bindings.dialog

    DEFAULT_CSS = """
        ClickResponse {
            align-horizontal: center;
            align-vertical:   middle;
            #frame {
                width:      auto;
                min-width:  60;
                border:     round $border;
                padding:    1 2;
                background: $background;
            }
            #prompt-row {
                width: 100%;
            }
            #prompt {
            }
            #button-row {
                width:      100%;
                margin-top: 2;
            }
            .button:first-child {
                margin-left:  0;
                margin-right: 4;
            }
            .button {
                margin-left:  4;
                margin-right: 4;
            }
            .button:last-child {
                margin-left:  4;
                margin-right: 0;
            }
        }
    """

    def __init__(self,
        prompt:   str,
        buttons:  Sequence[str] = ('Yes',     'No'),
        variants: Sequence[str] = ('primary', 'default'),
        **kwargs: Any,
    ):
        self.prompt   = prompt
        self.buttons  = buttons
        self.variants = variants
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        """Composes the dialog."""
        with VerticalGroup(id='frame'):
            with HorizontalGroup(id='prompt-row'):
                yield Label(self.prompt, id='prompt', shrink=True)
            with HorizontalGroup(id='button-row'):
                for (button, variant) in zip(
                    self.buttons, self.variants, strict=True
                ):
                    yield Button(
                        button, variant=variant,
                        id=button, classes='button',
                    )

    def on_button_pressed(self, event: Button.Pressed):
        """Reports to the caller which button the user pressed."""
        self.dismiss(event.button.id)

    def action_cancel(self):
        """Dismisses the dialog without a response to the caller."""
        self.dismiss()
