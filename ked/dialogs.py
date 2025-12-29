"""Pop-up dialogs used throughout the app"""

from . import bindings

from textual.screen     import ModalScreen
from textual.widgets    import Button
from textual.widgets    import Label
from textual.widgets    import Input
from textual.containers import VerticalGroup
from textual.containers import HorizontalGroup
from textual.containers import Center
from textual.containers import Right
from textual.app        import ComposeResult

from collections.abc import Sequence
from typing          import Any


class MessageBox(ModalScreen[None]):
    """Pop-up that displays a message/warning/error to the user."""

    BINDINGS = bindings.dialog

    DEFAULT_CSS = """
        MessageBox {
            align-horizontal: center;
            align-vertical:   middle;
            background:       black 20%;
            #frame {
                width:      auto;
                max-width:  60;
                border:     round $border;
                background: $background;
                padding:    1 2;
                align:      center middle;
            }
            #message-row {
            }
            #message {
            }
            #button-row {
                margin-top: 2;
            }
            #button {
            }
        }
    """

    def __init__(self,
        message:  str,
        title:    str = '',
        button:   str = 'Okay',
        **kwargs: Any,
    ):
        self.message = message
        self.title_  = title
        self.button  = button
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        """Composes the message box."""
        with VerticalGroup(id='frame') as frame:
            if self.title_:
                frame.border_title = self.title_
            with Center(id='message-row'):
                yield Label(self.message, id='message', shrink=True)
            with Center(id='button-row'):
                yield Button(self.button, id='button')

    def on_button_pressed(self, _event: Button.Pressed):
        """Closes the message box when the user pressed the button."""
        self.dismiss()

    def action_cancel(self):
        """Closes the message box when the user pressed Esc."""
        self.dismiss()


class ClickResponse(ModalScreen[str]):
    """Dialog asking the user to click a button to respond."""

    BINDINGS = bindings.dialog

    DEFAULT_CSS = """
        ClickResponse {
            align-horizontal: center;
            align-vertical:   middle;
            background:       black 20%;
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


class TextInput(ModalScreen[str]):
    """Dialog asking the user to enter text."""

    BINDINGS = bindings.dialog

    DEFAULT_CSS = """
        TextInput {
            align-horizontal: center;
            align-vertical:   middle;
            background:       black 20%;
            #frame {
                width:      60;
                border:     round $border;
                background: $background;
                padding:    1 2;
            }
            #input-row {
                align-horizontal: left;
            }
            #label {
                height:                 100%;
                content-align-vertical: middle;
            }
            #input {
                width:       1fr;
                margin-left: 1;
                border:      round $border;
            }
            #button-row {
                margin-top: 2;
            }
            .button {
            }
            #accept {
            }
            #cancel {
            }
        }
    """

    def __init__(self,
        label_text:     str,
        initial_value:  str = '',
        accept_text:    str = 'Okay',
        accept_variant: str = 'primary',
        cancel_text:    str = 'Cancel',
        cancel_variant: str = 'default',
        **kwargs: Any,
    ):
        self.label_text     = label_text
        self.initial_value  = initial_value
        self.accept_text    = accept_text
        self.accept_variant = accept_variant
        self.cancel_text    = cancel_text
        self.cancel_variant = cancel_variant
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        """Composes the dialog."""
        with VerticalGroup(id='frame'):
            with HorizontalGroup(id='input-row'):
                yield Label(self.label_text, id='label')
                yield Input(
                    self.initial_value, select_on_focus=False, id='input'
                )
            with HorizontalGroup(id='button-row'):
                yield Button(
                    self.accept_text,
                    variant = self.accept_variant,
                    classes = 'button',
                    id      = 'accept',
                )
                with Right():
                    yield Button(
                        self.cancel_text,
                        variant = self.cancel_variant,
                        classes = 'button',
                        id      = 'cancel',
                    )

    def on_input_submitted(self):
        """Changes focus to first button when user entered a value."""
        self.query('Button').focus()

    def on_button_pressed(self, event: Button.Pressed):
        """Reports the value of the input widget to the caller."""
        match event.button.id:
            case 'accept':
                input = self.query_exactly_one('#input', expect_type=Input)
                if not input.value:
                    self.action_cancel()
                else:
                    self.dismiss(input.value)
            case 'cancel':
                self.action_cancel()

    def action_cancel(self):
        """Dismisses the dialog without a response to the caller."""
        self.dismiss()
