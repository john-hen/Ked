# Ked
*simple text editor for the terminal*

Ked is a single-file text editor that runs in the terminal. Its interface is
intentionally simple, while its default key bindings resemble those of desktop
applications.


## Installation

Install the application with the [UV] package manager:
```
uv tool install Ked
```

There are other ways to install the app, such as via [PipX] or even just [Pip].
But UV is recommended as it isolates and manages all dependencies, including
Python.

[UV]:   https://docs.astral.sh/uv
[PipX]: https://pipx.pypa.io
[Pip]:  https://pip.pypa.io


## Usage

Simply run
```
ked some_file.txt
```

to edit a file. Run `ked --help` to list further command-line options. Press
<kbd>F1</kbd> in the app for help on interactive usage.


## Why Ked?

I refuse to use [Vim] for the sake of my muscle memory, and [Nano] won't let me
rebind all the keys that I want.

As for the name, no particular reason. It was available on [PyPI], first and
foremost, is quick to type, and has "ed" in it, like "edit" or "editor".

[Vim]:  https://neovim.io
[Nano]: https://www.nano-editor.org
[PyPI]: https://pypi.org


## Development

Ked is built in Python on top of the excellent TUI framework [Textual]. It uses
[Cyclopts] for the command-line interface.

Debugging a TUI application can be tricky as the user interface blocks the
terminal. But it is often sufficient to look at log output. As explained [in
the Textual documentation][textual-log], open a second terminal session and in
it, start the Textual development console with:
```
uv run textual console --exclude SYSTEM --exclude EVENT --exclude DEBUG
```

In the original terminal, run the app via Textual with:
```
uv run textual run --dev ked:cli some_file.txt
```

The output from `self.log` inside Textual widgets will then appear in the
development console. The `uv run` part of the commands can be left out if the
virtual dev environment has been activated. More verbosity can be achieved by
not suppressing certain message categories in the `textual console` command.

[Textual]:     https://textual.textualize.io
[Cyclopts]:    https://cyclopts.readthedocs.io
[textual-log]: https://textual.textualize.io/guide/devtools/#textual-log


[![release](
    https://img.shields.io/pypi/v/Ked.svg?label=release)](
    https://pypi.python.org/pypi/Ked)
