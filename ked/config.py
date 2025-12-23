"""Persistent storage of configuration"""

from . import meta

import cyclopts
import platformdirs
import yaml
import ruamel.yaml

from pathlib import Path
from typing  import TypeAlias
from typing  import Literal


settings = {}
cli = cyclopts.App(
    name     = 'config',
    help     = 'Manage the configuration.',
    sort_key = 2,
)

user_dir      = platformdirs.user_config_path() / meta.name
global_dir    = platformdirs.site_config_path() / meta.name
settings_file = 'settings.yaml'

Setting:  TypeAlias = tuple[str, ...]
Value:    TypeAlias = str | float | int | bool
Settings: TypeAlias = dict[str, Value | 'Settings']


@cli.command()
def dir():
    """Show the configuration directory."""
    print(user_dir)


@cli.command()
def file():
    """Show the configuration file."""
    print(user_dir/settings_file)


def query(
    setting: Setting,
    source:  Literal['user', 'global', 'default', 'all'] = 'all',
) -> Value:
    """Queries the value of a `setting` from configuration `source` file(s)."""
    if not isinstance(setting, tuple):
        raise TypeError('Argument `setting` must be a tuple of strings.')
    if setting == ():
        raise ValueError('Argument `setting` cannot be an empty tuple.')
    here  = Path(__file__).parent
    match source:
        case 'user':
            folders = (user_dir,)
        case 'global':
            folders = (global_dir,)
        case 'default':
            folders = (here,)
        case 'all':
            folders = (user_dir, global_dir, here)
    for folder in folders:
        file = folder/settings_file
        if not file.exists():
            continue
        settings = yaml.safe_load(file.read_text(encoding='UTF-8-sig'))
        value    = query_value(setting, settings)
        if value is not None:
            break
    else:
        raise KeyError(f'Setting "{setting}" not found in configuration.')
    return value


def store(
    setting: Setting,
    value:   Value,
    target:  Literal['user', 'global'] = 'user',
):
    """Stores the `value` of a `setting` in `target` configuration file."""
    match target:
        case 'user':
            folder = user_dir
        case 'global':
            folder = global_dir

    file = folder/settings_file
    if not file.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text('', encoding='UTF-8-sig')

    # Use Ruamel's round-trip parser in order to preserve comments the user may
    # have added in the configuration file.
    parser = ruamel.yaml.YAML(typ='rt', pure=True)
    settings = parser.load(file)
    if not isinstance(settings, dict):
        # Ruamel's parser may return a string with the content of the file, for
        # example if it contains nothing but comments.
        settings = {}
    store_value(setting, value, settings)
    parser.dump(settings, file)


def query_value(setting: Setting, settings: Settings) -> Value | None:
    """Retrieves the value of the `setting` in the `settings` dictionary."""
    key = setting[0]
    if key not in settings:
        return None
    if len(setting) == 1:
        return settings[key]
    return query_value(setting[1:], settings[key])


def store_value(setting: Setting, value: Value, settings: Settings):
    """Stores the `value` of the `setting` in the `settings` dictionary."""
    key = setting[0]
    if len(setting) == 1:
        settings[key] = value
        return
    if key not in settings:
        settings[key] = {}
    store_value(setting[1:], value, settings[key])
