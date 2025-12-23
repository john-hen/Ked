"""Tests the `config` module."""

from ked import config

from pytest import raises
from pytest import fixture


@fixture(scope='module', autouse=True)
def temp_folder(tmp_path_factory):
    temp_folder       = tmp_path_factory.getbasetemp()
    config.user_dir   = temp_folder / 'user'
    config.global_dir = temp_folder / 'global'
    config.global_dir.mkdir()
    file = config.global_dir / config.settings_file
    file.write_text('theme:\n  app: "global_theme"\n', encoding='UTF-8-sig')


def test_query():
    app_theme_default = config.query(('theme', 'app'), source='default')
    assert app_theme_default == 'flexoki'

    syntax_theme_default = config.query(('theme', 'syntax'), source='default')
    assert syntax_theme_default == 'css'

    with raises(TypeError, match='must be a tuple'):
        config.query('theme')
    with raises(ValueError, match='cannot be an empty tuple'):
        config.query(())
    with raises(KeyError, match='not found'):
        config.query(('does', 'not', 'exist'), source='default')

    with raises(KeyError, match='not found'):
        config.query(('theme', 'app'), source='user')
    assert config.query(('theme', 'app'),    source='global') == 'global_theme'
    assert config.query(('theme', 'app'),    source='all')    == 'global_theme'
    assert config.query(('theme', 'syntax'), source='all')    == 'css'


def test_store():
    assert not config.user_dir.exists()
    with raises(KeyError, match='not found'):
        config.query(('theme', 'app'), source='user')

    config.store(('theme', 'app'), 'user_theme', target='user')

    assert config.user_dir.exists()
    assert (config.user_dir/config.settings_file).exists()
    assert config.query(('theme', 'app'), source='user') == 'user_theme'

    config.store(('theme', 'app'), 'new_theme', target='global')
    assert config.query(('theme', 'app'), source='global') == 'new_theme'
