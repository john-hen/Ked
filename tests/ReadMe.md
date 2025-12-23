# Test suite

This folder contains the automated test suite, most of which has yet to be
implemented. The `files` folder contains some text files currently used for
manual tests.


## Debugging

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

[textual-log]: https://textual.textualize.io/guide/devtools/#textual-log


## Releases

To release a new version:
- Bump version number in `pyproject.toml` or use `uv version --bump`.
- Add dedicated commit for the version bump.
- Publish to PyPI via GitHub Action.
- Create release on GitHub, tag it (like `0.3.0`), add release notes.
