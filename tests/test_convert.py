import pytest

from pyreq2rpm.pyreq2rpm import convert

@pytest.mark.parametrize(('arg', 'expected'), [
    (['foobar', '~=', '2.4.8'], '(foobar >= 2.4.8 with foobar < 2.5)'),
])
def test_convert(arg, expected):
    assert convert(*arg) == expected
