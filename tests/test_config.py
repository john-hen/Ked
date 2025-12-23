"""Tests the `config` module."""

from ked import config

from pytest import raises
from pytest import fixture


@fixture(scope='module', autouse=True)
def temp_folder(tmp_path_factory):
    temp_folder     = tmp_path_factory.getbasetemp()
    config.user_dir = temp_folder / 'user'
    config.site_dir = temp_folder / 'site'
    config.site_dir.mkdir()
    file = config.site_dir / config.file_name
    file.write_text('theme:\n  app: "site_theme"\n', encoding='UTF-8-sig')


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
    assert config.query(('theme', 'app'),    source='site') == 'site_theme'
    assert config.query(('theme', 'app'),    source='all')  == 'site_theme'
    assert config.query(('theme', 'syntax'), source='all')  == 'css'


def test_store():
    assert not config.user_dir.exists()
    with raises(KeyError, match='not found'):
        config.query(('theme', 'app'), source='user')

    config.store(('theme', 'app'), 'user_theme', target='user')

    assert config.user_dir.exists()
    assert (config.user_dir/config.file_name).exists()
    assert config.query(('theme', 'app'), source='user') == 'user_theme'

    config.store(('theme', 'app'), 'new_theme', target='site')
    assert config.query(('theme', 'app'), source='site') == 'new_theme'
