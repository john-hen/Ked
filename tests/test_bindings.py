"""Tests the `bindings` module."""

from ked import bindings


def test_key_display():
    assert bindings.key_display('x')                 == 'X'
    assert bindings.key_display('ctrl+x')            == '^X'
    assert bindings.key_display('ctrl+shift+x')      == 'Ctrl+Shift+X'
    assert bindings.key_display('home')              == 'Home'
    assert bindings.key_display('ctrl+home')         == '^Home'
    assert bindings.key_display('ctrl+shift+home')   == 'Ctrl+Shift+Home'
    assert bindings.key_display('escape')            == 'Esc'
    assert bindings.key_display('delete')            == 'Del'
    assert bindings.key_display('ctrl+delete')       == '^Del'
    assert bindings.key_display('pageup')            == 'PgUp'
    assert bindings.key_display('pagedown')          == 'PgDn'
    assert bindings.key_display('ctrl+pageup')       == '^PgUp'
    assert bindings.key_display('ctrl+shift+pageup') == 'Ctrl+Shift+PgUp'
