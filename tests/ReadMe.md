## Test suite

This folder will contain the automated test suite, the code for which has yet
to be written. The `files` folder contains some test files currently being
used when testing manually.


### Debugging

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
