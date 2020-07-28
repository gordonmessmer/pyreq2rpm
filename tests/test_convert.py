import pytest

import subprocess
from pyreq2rpm.pyreq2rpm import convert, convert_requirement

def run_rpmbuild(dep):
    e = subprocess.run(['rpmbuild', '--nobuild', '--define',
                        'dep_test {}'.format(dep),
                        'tests/data/dep.spec'],)
    return e.returncode

@pytest.mark.parametrize(('arg', 'expected'), [
    (['foobar', '~=', '2.4.8'], '(foobar >= 2.4.8 with foobar < 2.5)'),
    (['foobar', '~=', '2.4.8.0'], '(foobar >= 2.4.8 with foobar < 2.4.9)'),
    (['foobar', '~=', '2.4.8.1'], '(foobar >= 2.4.8.1 with foobar < 2.4.9)'),
    (['foobar', '~=', '2.4.8.*'], 'Invalid version'),
    (['foobar', '~=', '2.0'], '(foobar >= 2 with foobar < 3)'),
    (['foobar', '~=', '2'], 'Invalid version'),
    (['foobar', '~=', '2.*'], 'Invalid version'),
    (['foobar', '~=', '2.4.8b5'], '(foobar >= 2.4.8~b5 with foobar < 2.5)'),
    (['foobar', '~=', '2.0.0b5'], '(foobar >= 2~b5 with foobar < 2.1)'),
    (['foobar', '~=', '2.4.8.post1'], '(foobar >= 2.4.8^post1 with foobar < 2.5)'),
    (['foobar', '~=', '2.0.post1'], '(foobar >= 2^post1 with foobar < 3)'),
    (['foobar', '~=', '0.0'], '(foobar >= 0 with foobar < 1)'),
    (['foobar', '==', '2.4.8'], 'foobar = 2.4.8'),
    (['foobar', '==', '2.4.8.0'], 'foobar = 2.4.8'),
    (['foobar', '==', '2.4.8.1'], 'foobar = 2.4.8.1'),
    (['foobar', '==', '2.4.8.*'], '(foobar >= 2.4.8 with foobar < 2.4.9)'),
    (['foobar', '==', '2.0'], 'foobar = 2'),
    (['foobar', '==', '2'], 'foobar = 2'),
    (['foobar', '==', '2.*'], '(foobar >= 2 with foobar < 3)'),
    (['foobar', '==', '2.4.8b5'], 'foobar = 2.4.8~b5'),
    (['foobar', '==', '2.0.0b5'], 'foobar = 2~b5'),
    (['foobar', '==', '2.4.8.post1'], 'foobar = 2.4.8^post1'),
    (['foobar', '==', '2.0.post1'], 'foobar = 2^post1'),
    (['foobar', '==', '0.0'], 'foobar = 0'),
    (['foobar', '===', '2.4.8'], 'foobar = 2.4.8'),
    (['foobar', '===', '2.4.8.0'], 'foobar = 2.4.8'),
    (['foobar', '===', '2.4.8.1'], 'foobar = 2.4.8.1'),
    (['foobar', '===', '2.4.8.*'], 'Invalid version'),
    (['foobar', '===', '2.0'], 'foobar = 2'),
    (['foobar', '===', '2'], 'foobar = 2'),
    (['foobar', '===', '2.*'], 'Invalid version'),
    (['foobar', '===', '2.4.8b5'], 'foobar = 2.4.8~b5'),
    (['foobar', '===', '2.0.0b5'], 'foobar = 2~b5'),
    (['foobar', '===', '2.4.8.post1'], 'foobar = 2.4.8^post1'),
    (['foobar', '===', '2.0.post1'], 'foobar = 2^post1'),
    (['foobar', '===', '0.0'], 'foobar = 0'),
    (['foobar', '!=', '2.4.8'], '(foobar < 2.4.8 or foobar > 2.4.8)'),
    (['foobar', '!=', '2.4.8.0'], '(foobar < 2.4.8 or foobar > 2.4.8)'),
    (['foobar', '!=', '2.4.8.1'], '(foobar < 2.4.8.1 or foobar > 2.4.8.1)'),
    (['foobar', '!=', '2.4.8.*'], '(foobar < 2.4.8 or foobar > 2.4.9)'),
    (['foobar', '!=', '2.0'], '(foobar < 2 or foobar > 2)'),
    (['foobar', '!=', '2'], '(foobar < 2 or foobar > 2)'),
    (['foobar', '!=', '2.*'], '(foobar < 2 or foobar > 3)'),
    (['foobar', '!=', '2.4.8b5'], '(foobar < 2.4.8~b5 or foobar > 2.4.8~b5)'),
    (['foobar', '!=', '2.0.0b5'], '(foobar < 2~b5 or foobar > 2~b5)'),
    (['foobar', '!=', '2.4.8.post1'], '(foobar < 2.4.8^post1 or foobar > 2.4.8^post1)'),
    (['foobar', '!=', '2.0.post1'], '(foobar < 2^post1 or foobar > 2^post1)'),
    (['foobar', '!=', '0.0'], '(foobar < 0 or foobar > 0)'),
    (['foobar', '<=', '2.4.8'], 'foobar <= 2.4.8'),
    (['foobar', '<=', '2.4.8.0'], 'foobar <= 2.4.8'),
    (['foobar', '<=', '2.4.8.1'], 'foobar <= 2.4.8.1'),
    (['foobar', '<=', '2.4.8.*'], 'foobar < 2.4.8'), # see notes in pyreq2rpm.convert_ordered
    (['foobar', '<=', '2.0'], 'foobar <= 2'),
    (['foobar', '<=', '2'], 'foobar <= 2'),
    (['foobar', '<=', '2.*'], 'foobar < 2'), # see notes in pyreq2rpm.convert_ordered
    (['foobar', '<=', '2.4.8b5'], 'foobar <= 2.4.8~b5'),
    (['foobar', '<=', '2.0.0b5'], 'foobar <= 2~b5'),
    (['foobar', '<=', '2.4.8.post1'], 'foobar <= 2.4.8^post1'),
    (['foobar', '<=', '2.0.post1'], 'foobar <= 2^post1'),
    (['foobar', '<=', '0.0'], 'foobar <= 0'),
    (['foobar', '<', '2.4.8'], 'foobar < 2.4.8'),
    (['foobar', '<', '2.4.8.0'], 'foobar < 2.4.8'),
    (['foobar', '<', '2.4.8.1'], 'foobar < 2.4.8.1'),
    (['foobar', '<', '2.4.8.*'], 'foobar < 2.4.8'),
    (['foobar', '<', '2.0'], 'foobar < 2'),
    (['foobar', '<', '2'], 'foobar < 2'),
    (['foobar', '<', '2.*'], 'foobar < 2'),
    (['foobar', '<', '2.4.8b5'], 'foobar < 2.4.8~b5'),
    (['foobar', '<', '2.0.0b5'], 'foobar < 2~b5'),
    (['foobar', '<', '2.4.8.post1'], 'foobar < 2.4.8^post1'),
    (['foobar', '<', '2.0.post1'], 'foobar < 2^post1'),
    (['foobar', '<', '0.0'], 'foobar < 0'),
    (['foobar', '>=', '2.4.8'], 'foobar >= 2.4.8'),
    (['foobar', '>=', '2.4.8.0'], 'foobar >= 2.4.8'),
    (['foobar', '>=', '2.4.8.1'], 'foobar >= 2.4.8.1'),
    (['foobar', '>=', '2.4.8.*'], 'foobar >= 2.4.8'),
    (['foobar', '>=', '2.0'], 'foobar >= 2'),
    (['foobar', '>=', '2'], 'foobar >= 2'),
    (['foobar', '>=', '2.*'], 'foobar >= 2'),
    (['foobar', '>=', '2.4.8b5'], 'foobar >= 2.4.8~b5'),
    (['foobar', '>=', '2.0.0b5'], 'foobar >= 2~b5'),
    (['foobar', '>=', '2.4.8.post1'], 'foobar >= 2.4.8^post1'),
    (['foobar', '>=', '2.0.post1'], 'foobar >= 2^post1'),
    (['foobar', '>=', '0.0'], 'foobar >= 0'),
    (['foobar', '>', '2.4.8'], 'foobar > 2.4.8'),
    (['foobar', '>', '2.4.8.0'], 'foobar > 2.4.8'),
    (['foobar', '>', '2.4.8.1'], 'foobar > 2.4.8.1'),
    (['foobar', '>', '2.4.8.*'], 'foobar >= 2.4.8'), # see notes in pyreq2rpm.convert_ordered
    (['foobar', '>', '2.0'], 'foobar > 2'),
    (['foobar', '>', '2'], 'foobar > 2'),
    (['foobar', '>', '2.*'], 'foobar >= 2'), # see notes in pyreq2rpm.convert_ordered
    (['foobar', '>', '2.4.8b5'], 'foobar > 2.4.8~b5'),
    (['foobar', '>', '2.0.0b5'], 'foobar > 2~b5'),
    (['foobar', '>', '2.4.8.post1'], 'foobar > 2.4.8^post1'),
    (['foobar', '>', '2.0.post1'], 'foobar > 2^post1'),
    (['foobar', '>', '0.0'], 'foobar > 0'),
    (['foobar', '>', '1.0.0.dev4'], 'foobar > 1~~dev4'),
    (['foobar', '>', '1.1.1a2'], 'foobar > 1.1.1~a2'),
    (['foobar', '>', '1.1.0rc3'], 'foobar > 1.1~rc3'),
])
def test_convert(arg, expected):
    assert convert(*arg) == expected
    assert run_rpmbuild(convert(*arg)) == 0

@pytest.mark.parametrize(('arg', 'expected'), [
    ('pyparsing', 'pyparsing'),
    ('pyparsing>=2.0.1,!=2.0.4,!=2.1.2,!=2.1.6',
     '((pyparsing < 2.0.4 or pyparsing > 2.0.4)'
     ' with (pyparsing < 2.1.2 or pyparsing > 2.1.2)'
     ' with (pyparsing < 2.1.6 or pyparsing > 2.1.6)'
     ' with pyparsing >= 2.0.1)'),
    ('babel>=1.3,!=2.0', '((babel < 2 or babel > 2) with babel >= 1.3)'),
])
def test_convert_requirement(arg, expected):
    assert convert_requirement(arg) == expected
    assert run_rpmbuild(convert_requirement(arg)) == 0
