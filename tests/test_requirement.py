import pytest

import pkg_resources
import subprocess
from pyreq2rpm.pyreq2rpm import RpmVersion, convert

@pytest.mark.parametrize(('version', 'op', 'arg', 'expected'), [
    ('2.4.8', '~=', '2.4.8', True),
    ('2.4.8.0', '~=', '2.4.8', True),
    ('2.4.8.1', '~=', '2.4.8', True),
    ('2.4.8b5', '~=', '2.4.8', False),
    ('2.4.8.post1', '~=', '2.4.8', True),
    ('2.0', '~=', '2.4.8', False),
    ('2', '~=', '2.4.8', False),
    ('2.0.0b5', '~=', '2.4.8', False),
    ('2.0.post1', '~=', '2.4.8', False),
    ('2.4.8', '~=', '2.4.8.0', True),
    ('2.4.8.0', '~=', '2.4.8.0', True),
    ('2.4.8.1', '~=', '2.4.8.0', True),
    ('2.4.8b5', '~=', '2.4.8.0', False),
    ('2.4.8.post1', '~=', '2.4.8.0', True),
    ('2.0', '~=', '2.4.8.0', False),
    ('2', '~=', '2.4.8.0', False),
    ('2.0.0b5', '~=', '2.4.8.0', False),
    ('2.0.post1', '~=', '2.4.8.0', False),
    ('2.4.8', '~=', '2.4.8.1', False),
    ('2.4.8.0', '~=', '2.4.8.1', False),
    ('2.4.8.1', '~=', '2.4.8.1', True),
    ('2.4.8b5', '~=', '2.4.8.1', False),
    ('2.4.8.post1', '~=', '2.4.8.1', False),
    ('2.0', '~=', '2.4.8.1', False),
    ('2', '~=', '2.4.8.1', False),
    ('2.0.0b5', '~=', '2.4.8.1', False),
    ('2.0.post1', '~=', '2.4.8.1', False),
    ('2.4.8', '~=', '2.4.8b5', True),
    ('2.4.8.0', '~=', '2.4.8b5', True),
    ('2.4.8.1', '~=', '2.4.8b5', True),
    ('2.4.8b5', '~=', '2.4.8b5', True),
    ('2.4.8.post1', '~=', '2.4.8b5', True),
    ('2.0', '~=', '2.4.8b5', False),
    ('2', '~=', '2.4.8b5', False),
    ('2.0.0b5', '~=', '2.4.8b5', False),
    ('2.0.post1', '~=', '2.4.8b5', False),
    ('2.4.8', '~=', '2.4.8.post1', False),
    ('2.4.8.0', '~=', '2.4.8.post1', False),
    ('2.4.8.1', '~=', '2.4.8.post1', True),
    ('2.4.8b5', '~=', '2.4.8.post1', False),
    ('2.4.8.post1', '~=', '2.4.8.post1', True),
    ('2.0', '~=', '2.4.8.post1', False),
    ('2', '~=', '2.4.8.post1', False),
    ('2.0.0b5', '~=', '2.4.8.post1', False),
    ('2.0.post1', '~=', '2.4.8.post1', False),
    ('2.4.8', '~=', '2.0', True),
    ('2.4.8.0', '~=', '2.0', True),
    ('2.4.8.1', '~=', '2.0', True),
    ('2.4.8b5', '~=', '2.0', True),
    ('2.4.8.post1', '~=', '2.0', True),
    ('2.0', '~=', '2.0', True),
    ('2', '~=', '2.0', True),
    ('2.0.0b5', '~=', '2.0', False),
    ('2.0.post1', '~=', '2.0', True),
    ('2.4.8', '~=', '2.0.0b5', False),
    ('2.4.8.0', '~=', '2.0.0b5', False),
    ('2.4.8.1', '~=', '2.0.0b5', False),
    ('2.4.8b5', '~=', '2.0.0b5', False),
    ('2.4.8.post1', '~=', '2.0.0b5', False),
    ('2.0', '~=', '2.0.0b5', True),
    ('2', '~=', '2.0.0b5', True),
    ('2.0.0b5', '~=', '2.0.0b5', True),
    ('2.0.post1', '~=', '2.0.0b5', False),
    ('2.4.8', '~=', '2.0.post1', True),
    ('2.4.8.0', '~=', '2.0.post1', True),
    ('2.4.8.1', '~=', '2.0.post1', True),
    ('2.4.8b5', '~=', '2.0.post1', True),
    ('2.4.8.post1', '~=', '2.0.post1', True),
    ('2.0', '~=', '2.0.post1', False),
    ('2', '~=', '2.0.post1', False),
    ('2.0.0b5', '~=', '2.0.post1', False),
    ('2.0.post1', '~=', '2.0.post1', True),
    ('2.4.8', '==', '2.4.8', True),
    ('2.4.8.0', '==', '2.4.8', True),
    ('2.4.8.1', '==', '2.4.8', False),
    ('2.4.8b5', '==', '2.4.8', False),
    ('2.4.8.post1', '==', '2.4.8', False),
    ('2.0', '==', '2.4.8', False),
    ('2', '==', '2.4.8', False),
    ('2.0.0b5', '==', '2.4.8', False),
    ('2.0.post1', '==', '2.4.8', False),
    ('2.4.8', '==', '2.4.8.0', True),
    ('2.4.8.0', '==', '2.4.8.0', True),
    ('2.4.8.1', '==', '2.4.8.0', False),
    ('2.4.8b5', '==', '2.4.8.0', False),
    ('2.4.8.post1', '==', '2.4.8.0', False),
    ('2.0', '==', '2.4.8.0', False),
    ('2', '==', '2.4.8.0', False),
    ('2.0.0b5', '==', '2.4.8.0', False),
    ('2.0.post1', '==', '2.4.8.0', False),
    ('2.4.8', '==', '2.4.8.1', False),
    ('2.4.8.0', '==', '2.4.8.1', False),
    ('2.4.8.1', '==', '2.4.8.1', True),
    ('2.4.8b5', '==', '2.4.8.1', False),
    ('2.4.8.post1', '==', '2.4.8.1', False),
    ('2.0', '==', '2.4.8.1', False),
    ('2', '==', '2.4.8.1', False),
    ('2.0.0b5', '==', '2.4.8.1', False),
    ('2.0.post1', '==', '2.4.8.1', False),
    ('2.4.8', '==', '2.4.8.*', True),
    ('2.4.8.0', '==', '2.4.8.*', True),
    ('2.4.8.1', '==', '2.4.8.*', True),
    ('2.4.8b5', '==', '2.4.8.*', True),
    ('2.4.8.post1', '==', '2.4.8.*', True),
    ('2.0', '==', '2.4.8.*', False),
    ('2', '==', '2.4.8.*', False),
    ('2.0.0b5', '==', '2.4.8.*', False),
    ('2.0.post1', '==', '2.4.8.*', False),
    ('2.4.8', '==', '2.4.8b5', False),
    ('2.4.8.0', '==', '2.4.8b5', False),
    ('2.4.8.1', '==', '2.4.8b5', False),
    ('2.4.8b5', '==', '2.4.8b5', True),
    ('2.4.8.post1', '==', '2.4.8b5', False),
    ('2.0', '==', '2.4.8b5', False),
    ('2', '==', '2.4.8b5', False),
    ('2.0.0b5', '==', '2.4.8b5', False),
    ('2.0.post1', '==', '2.4.8b5', False),
    ('2.4.8', '==', '2.4.8.post1', False),
    ('2.4.8.0', '==', '2.4.8.post1', False),
    ('2.4.8.1', '==', '2.4.8.post1', False),
    ('2.4.8b5', '==', '2.4.8.post1', False),
    ('2.4.8.post1', '==', '2.4.8.post1', True),
    ('2.0', '==', '2.4.8.post1', False),
    ('2', '==', '2.4.8.post1', False),
    ('2.0.0b5', '==', '2.4.8.post1', False),
    ('2.0.post1', '==', '2.4.8.post1', False),
    ('2.4.8', '==', '2.0', False),
    ('2.4.8.0', '==', '2.0', False),
    ('2.4.8.1', '==', '2.0', False),
    ('2.4.8b5', '==', '2.0', False),
    ('2.4.8.post1', '==', '2.0', False),
    ('2.0', '==', '2.0', True),
    ('2', '==', '2.0', True),
    ('2.0.0b5', '==', '2.0', False),
    ('2.0.post1', '==', '2.0', False),
    ('2.4.8', '==', '2', False),
    ('2.4.8.0', '==', '2', False),
    ('2.4.8.1', '==', '2', False),
    ('2.4.8b5', '==', '2', False),
    ('2.4.8.post1', '==', '2', False),
    ('2.0', '==', '2', True),
    ('2', '==', '2', True),
    ('2.0.0b5', '==', '2', False),
    ('2.0.post1', '==', '2', False),
    ('2.4.8', '==', '2.*', True),
    ('2.4.8.0', '==', '2.*', True),
    ('2.4.8.1', '==', '2.*', True),
    ('2.4.8b5', '==', '2.*', True),
    ('2.4.8.post1', '==', '2.*', True),
    ('2.0', '==', '2.*', True),
    ('2', '==', '2.*', True),
    ('2.0.0b5', '==', '2.*', True),
    ('2.0.post1', '==', '2.*', True),
    ('2.4.8', '==', '2.0.0b5', False),
    ('2.4.8.0', '==', '2.0.0b5', False),
    ('2.4.8.1', '==', '2.0.0b5', False),
    ('2.4.8b5', '==', '2.0.0b5', False),
    ('2.4.8.post1', '==', '2.0.0b5', False),
    ('2.0', '==', '2.0.0b5', False),
    ('2', '==', '2.0.0b5', False),
    ('2.0.0b5', '==', '2.0.0b5', True),
    ('2.0.post1', '==', '2.0.0b5', False),
    ('2.4.8', '==', '2.0.post1', False),
    ('2.4.8.0', '==', '2.0.post1', False),
    ('2.4.8.1', '==', '2.0.post1', False),
    ('2.4.8b5', '==', '2.0.post1', False),
    ('2.4.8.post1', '==', '2.0.post1', False),
    ('2.0', '==', '2.0.post1', False),
    ('2', '==', '2.0.post1', False),
    ('2.0.0b5', '==', '2.0.post1', False),
    ('2.0.post1', '==', '2.0.post1', True),
    ('2.4.8', '===', '2.4.8', True),
    ('2.4.8.0', '===', '2.4.8', False),
    ('2.4.8.1', '===', '2.4.8', False),
    ('2.4.8b5', '===', '2.4.8', False),
    ('2.4.8.post1', '===', '2.4.8', False),
    ('2.0', '===', '2.4.8', False),
    ('2', '===', '2.4.8', False),
    ('2.0.0b5', '===', '2.4.8', False),
    ('2.0.post1', '===', '2.4.8', False),
    ('2.4.8', '===', '2.4.8.0', False),
    ('2.4.8.0', '===', '2.4.8.0', True),
    ('2.4.8.1', '===', '2.4.8.0', False),
    ('2.4.8b5', '===', '2.4.8.0', False),
    ('2.4.8.post1', '===', '2.4.8.0', False),
    ('2.0', '===', '2.4.8.0', False),
    ('2', '===', '2.4.8.0', False),
    ('2.0.0b5', '===', '2.4.8.0', False),
    ('2.0.post1', '===', '2.4.8.0', False),
    ('2.4.8', '===', '2.4.8.1', False),
    ('2.4.8.0', '===', '2.4.8.1', False),
    ('2.4.8.1', '===', '2.4.8.1', True),
    ('2.4.8b5', '===', '2.4.8.1', False),
    ('2.4.8.post1', '===', '2.4.8.1', False),
    ('2.0', '===', '2.4.8.1', False),
    ('2', '===', '2.4.8.1', False),
    ('2.0.0b5', '===', '2.4.8.1', False),
    ('2.0.post1', '===', '2.4.8.1', False),
    ('2.4.8', '===', '2.4.8.*', False),
    ('2.4.8.0', '===', '2.4.8.*', False),
    ('2.4.8.1', '===', '2.4.8.*', False),
    ('2.4.8b5', '===', '2.4.8.*', False),
    ('2.4.8.post1', '===', '2.4.8.*', False),
    ('2.0', '===', '2.4.8.*', False),
    ('2', '===', '2.4.8.*', False),
    ('2.0.0b5', '===', '2.4.8.*', False),
    ('2.0.post1', '===', '2.4.8.*', False),
    ('2.4.8', '===', '2.4.8b5', False),
    ('2.4.8.0', '===', '2.4.8b5', False),
    ('2.4.8.1', '===', '2.4.8b5', False),
    ('2.4.8b5', '===', '2.4.8b5', True),
    ('2.4.8.post1', '===', '2.4.8b5', False),
    ('2.0', '===', '2.4.8b5', False),
    ('2', '===', '2.4.8b5', False),
    ('2.0.0b5', '===', '2.4.8b5', False),
    ('2.0.post1', '===', '2.4.8b5', False),
    ('2.4.8', '===', '2.4.8.post1', False),
    ('2.4.8.0', '===', '2.4.8.post1', False),
    ('2.4.8.1', '===', '2.4.8.post1', False),
    ('2.4.8b5', '===', '2.4.8.post1', False),
    ('2.4.8.post1', '===', '2.4.8.post1', True),
    ('2.0', '===', '2.4.8.post1', False),
    ('2', '===', '2.4.8.post1', False),
    ('2.0.0b5', '===', '2.4.8.post1', False),
    ('2.0.post1', '===', '2.4.8.post1', False),
    ('2.4.8', '===', '2.0', False),
    ('2.4.8.0', '===', '2.0', False),
    ('2.4.8.1', '===', '2.0', False),
    ('2.4.8b5', '===', '2.0', False),
    ('2.4.8.post1', '===', '2.0', False),
    ('2.0', '===', '2.0', True),
    ('2', '===', '2.0', False),
    ('2.0.0b5', '===', '2.0', False),
    ('2.0.post1', '===', '2.0', False),
    ('2.4.8', '===', '2', False),
    ('2.4.8.0', '===', '2', False),
    ('2.4.8.1', '===', '2', False),
    ('2.4.8b5', '===', '2', False),
    ('2.4.8.post1', '===', '2', False),
    ('2.0', '===', '2', False),
    ('2', '===', '2', True),
    ('2.0.0b5', '===', '2', False),
    ('2.0.post1', '===', '2', False),
    ('2.4.8', '===', '2.*', False),
    ('2.4.8.0', '===', '2.*', False),
    ('2.4.8.1', '===', '2.*', False),
    ('2.4.8b5', '===', '2.*', False),
    ('2.4.8.post1', '===', '2.*', False),
    ('2.0', '===', '2.*', False),
    ('2', '===', '2.*', False),
    ('2.0.0b5', '===', '2.*', False),
    ('2.0.post1', '===', '2.*', False),
    ('2.4.8', '===', '2.0.0b5', False),
    ('2.4.8.0', '===', '2.0.0b5', False),
    ('2.4.8.1', '===', '2.0.0b5', False),
    ('2.4.8b5', '===', '2.0.0b5', False),
    ('2.4.8.post1', '===', '2.0.0b5', False),
    ('2.0', '===', '2.0.0b5', False),
    ('2', '===', '2.0.0b5', False),
    ('2.0.0b5', '===', '2.0.0b5', True),
    ('2.0.post1', '===', '2.0.0b5', False),
    ('2.4.8', '===', '2.0.post1', False),
    ('2.4.8.0', '===', '2.0.post1', False),
    ('2.4.8.1', '===', '2.0.post1', False),
    ('2.4.8b5', '===', '2.0.post1', False),
    ('2.4.8.post1', '===', '2.0.post1', False),
    ('2.0', '===', '2.0.post1', False),
    ('2', '===', '2.0.post1', False),
    ('2.0.0b5', '===', '2.0.post1', False),
    ('2.0.post1', '===', '2.0.post1', True),
    ('2.4.8', '!=', '2.4.8', False),
    ('2.4.8.0', '!=', '2.4.8', False),
    ('2.4.8.1', '!=', '2.4.8', True),
    ('2.4.8b5', '!=', '2.4.8', True),
    ('2.4.8.post1', '!=', '2.4.8', True),
    ('2.0', '!=', '2.4.8', True),
    ('2', '!=', '2.4.8', True),
    ('2.0.0b5', '!=', '2.4.8', True),
    ('2.0.post1', '!=', '2.4.8', True),
    ('2.4.8', '!=', '2.4.8.0', False),
    ('2.4.8.0', '!=', '2.4.8.0', False),
    ('2.4.8.1', '!=', '2.4.8.0', True),
    ('2.4.8b5', '!=', '2.4.8.0', True),
    ('2.4.8.post1', '!=', '2.4.8.0', True),
    ('2.0', '!=', '2.4.8.0', True),
    ('2', '!=', '2.4.8.0', True),
    ('2.0.0b5', '!=', '2.4.8.0', True),
    ('2.0.post1', '!=', '2.4.8.0', True),
    ('2.4.8', '!=', '2.4.8.1', True),
    ('2.4.8.0', '!=', '2.4.8.1', True),
    ('2.4.8.1', '!=', '2.4.8.1', False),
    ('2.4.8b5', '!=', '2.4.8.1', True),
    ('2.4.8.post1', '!=', '2.4.8.1', True),
    ('2.0', '!=', '2.4.8.1', True),
    ('2', '!=', '2.4.8.1', True),
    ('2.0.0b5', '!=', '2.4.8.1', True),
    ('2.0.post1', '!=', '2.4.8.1', True),
    ('2.4.8', '!=', '2.4.8.*', False),
    ('2.4.8.0', '!=', '2.4.8.*', False),
    ('2.4.8.1', '!=', '2.4.8.*', False),
    ('2.4.8b5', '!=', '2.4.8.*', False),
    ('2.4.8.post1', '!=', '2.4.8.*', False),
    ('2.0', '!=', '2.4.8.*', True),
    ('2', '!=', '2.4.8.*', True),
    ('2.0.0b5', '!=', '2.4.8.*', True),
    ('2.0.post1', '!=', '2.4.8.*', True),
    ('2.4.8', '!=', '2.4.8b5', True),
    ('2.4.8.0', '!=', '2.4.8b5', True),
    ('2.4.8.1', '!=', '2.4.8b5', True),
    ('2.4.8b5', '!=', '2.4.8b5', False),
    ('2.4.8.post1', '!=', '2.4.8b5', True),
    ('2.0', '!=', '2.4.8b5', True),
    ('2', '!=', '2.4.8b5', True),
    ('2.0.0b5', '!=', '2.4.8b5', True),
    ('2.0.post1', '!=', '2.4.8b5', True),
    ('2.4.8', '!=', '2.4.8.post1', True),
    ('2.4.8.0', '!=', '2.4.8.post1', True),
    ('2.4.8.1', '!=', '2.4.8.post1', True),
    ('2.4.8b5', '!=', '2.4.8.post1', True),
    ('2.4.8.post1', '!=', '2.4.8.post1', False),
    ('2.0', '!=', '2.4.8.post1', True),
    ('2', '!=', '2.4.8.post1', True),
    ('2.0.0b5', '!=', '2.4.8.post1', True),
    ('2.0.post1', '!=', '2.4.8.post1', True),
    ('2.4.8', '!=', '2.0', True),
    ('2.4.8.0', '!=', '2.0', True),
    ('2.4.8.1', '!=', '2.0', True),
    ('2.4.8b5', '!=', '2.0', True),
    ('2.4.8.post1', '!=', '2.0', True),
    ('2.0', '!=', '2.0', False),
    ('2', '!=', '2.0', False),
    ('2.0.0b5', '!=', '2.0', True),
    ('2.0.post1', '!=', '2.0', True),
    ('2.4.8', '!=', '2', True),
    ('2.4.8.0', '!=', '2', True),
    ('2.4.8.1', '!=', '2', True),
    ('2.4.8b5', '!=', '2', True),
    ('2.4.8.post1', '!=', '2', True),
    ('2.0', '!=', '2', False),
    ('2', '!=', '2', False),
    ('2.0.0b5', '!=', '2', True),
    ('2.0.post1', '!=', '2', True),
    ('2.4.8', '!=', '2.*', False),
    ('2.4.8.0', '!=', '2.*', False),
    ('2.4.8.1', '!=', '2.*', False),
    ('2.4.8b5', '!=', '2.*', False),
    ('2.4.8.post1', '!=', '2.*', False),
    ('2.0', '!=', '2.*', False),
    ('2', '!=', '2.*', False),
    ('2.0.0b5', '!=', '2.*', False),
    ('2.0.post1', '!=', '2.*', False),
    ('2.4.8', '!=', '2.0.0b5', True),
    ('2.4.8.0', '!=', '2.0.0b5', True),
    ('2.4.8.1', '!=', '2.0.0b5', True),
    ('2.4.8b5', '!=', '2.0.0b5', True),
    ('2.4.8.post1', '!=', '2.0.0b5', True),
    ('2.0', '!=', '2.0.0b5', True),
    ('2', '!=', '2.0.0b5', True),
    ('2.0.0b5', '!=', '2.0.0b5', False),
    ('2.0.post1', '!=', '2.0.0b5', True),
    ('2.4.8', '!=', '2.0.post1', True),
    ('2.4.8.0', '!=', '2.0.post1', True),
    ('2.4.8.1', '!=', '2.0.post1', True),
    ('2.4.8b5', '!=', '2.0.post1', True),
    ('2.4.8.post1', '!=', '2.0.post1', True),
    ('2.0', '!=', '2.0.post1', True),
    ('2', '!=', '2.0.post1', True),
    ('2.0.0b5', '!=', '2.0.post1', True),
    ('2.0.post1', '!=', '2.0.post1', False),
    ('2.4.8', '<=', '2.4.8', True),
    ('2.4.8.0', '<=', '2.4.8', True),
    ('2.4.8.1', '<=', '2.4.8', False),
    ('2.4.8b5', '<=', '2.4.8', True),
    ('2.4.8.post1', '<=', '2.4.8', False),
    ('2.0', '<=', '2.4.8', True),
    ('2', '<=', '2.4.8', True),
    ('2.0.0b5', '<=', '2.4.8', True),
    ('2.0.post1', '<=', '2.4.8', True),
    ('2.4.8', '<=', '2.4.8.0', True),
    ('2.4.8.0', '<=', '2.4.8.0', True),
    ('2.4.8.1', '<=', '2.4.8.0', False),
    ('2.4.8b5', '<=', '2.4.8.0', True),
    ('2.4.8.post1', '<=', '2.4.8.0', False),
    ('2.0', '<=', '2.4.8.0', True),
    ('2', '<=', '2.4.8.0', True),
    ('2.0.0b5', '<=', '2.4.8.0', True),
    ('2.0.post1', '<=', '2.4.8.0', True),
    ('2.4.8', '<=', '2.4.8.1', True),
    ('2.4.8.0', '<=', '2.4.8.1', True),
    ('2.4.8.1', '<=', '2.4.8.1', True),
    ('2.4.8b5', '<=', '2.4.8.1', True),
    ('2.4.8.post1', '<=', '2.4.8.1', True),
    ('2.0', '<=', '2.4.8.1', True),
    ('2', '<=', '2.4.8.1', True),
    ('2.0.0b5', '<=', '2.4.8.1', True),
    ('2.0.post1', '<=', '2.4.8.1', True),
    ('2.4.8', '<=', '2.4.8.*', False),
    ('2.4.8.0', '<=', '2.4.8.*', False),
    ('2.4.8.1', '<=', '2.4.8.*', False),
    ('2.4.8b5', '<=', '2.4.8.*', False),
    ('2.4.8.post1', '<=', '2.4.8.*', False),
    ('2.0', '<=', '2.4.8.*', True),
    ('2', '<=', '2.4.8.*', True),
    ('2.0.0b5', '<=', '2.4.8.*', True),
    ('2.0.post1', '<=', '2.4.8.*', True),
    ('2.4.8', '<=', '2.4.8b5', False),
    ('2.4.8.0', '<=', '2.4.8b5', False),
    ('2.4.8.1', '<=', '2.4.8b5', False),
    ('2.4.8b5', '<=', '2.4.8b5', True),
    ('2.4.8.post1', '<=', '2.4.8b5', False),
    ('2.0', '<=', '2.4.8b5', True),
    ('2', '<=', '2.4.8b5', True),
    ('2.0.0b5', '<=', '2.4.8b5', True),
    ('2.0.post1', '<=', '2.4.8b5', True),
    ('2.4.8', '<=', '2.4.8.post1', True),
    ('2.4.8.0', '<=', '2.4.8.post1', True),
    ('2.4.8.1', '<=', '2.4.8.post1', False),
    ('2.4.8b5', '<=', '2.4.8.post1', True),
    ('2.4.8.post1', '<=', '2.4.8.post1', True),
    ('2.0', '<=', '2.4.8.post1', True),
    ('2', '<=', '2.4.8.post1', True),
    ('2.0.0b5', '<=', '2.4.8.post1', True),
    ('2.0.post1', '<=', '2.4.8.post1', True),
    ('2.4.8', '<=', '2.0', False),
    ('2.4.8.0', '<=', '2.0', False),
    ('2.4.8.1', '<=', '2.0', False),
    ('2.4.8b5', '<=', '2.0', False),
    ('2.4.8.post1', '<=', '2.0', False),
    ('2.0', '<=', '2.0', True),
    ('2', '<=', '2.0', True),
    ('2.0.0b5', '<=', '2.0', True),
    ('2.0.post1', '<=', '2.0', False),
    ('2.4.8', '<=', '2', False),
    ('2.4.8.0', '<=', '2', False),
    ('2.4.8.1', '<=', '2', False),
    ('2.4.8b5', '<=', '2', False),
    ('2.4.8.post1', '<=', '2', False),
    ('2.0', '<=', '2', True),
    ('2', '<=', '2', True),
    ('2.0.0b5', '<=', '2', True),
    ('2.0.post1', '<=', '2', False),
    ('2.4.8', '<=', '2.*', False),
    ('2.4.8.0', '<=', '2.*', False),
    ('2.4.8.1', '<=', '2.*', False),
    ('2.4.8b5', '<=', '2.*', False),
    ('2.4.8.post1', '<=', '2.*', False),
    ('2.0', '<=', '2.*', False),
    ('2', '<=', '2.*', False),
    ('2.0.0b5', '<=', '2.*', False),
    ('2.0.post1', '<=', '2.*', False),
    ('2.4.8', '<=', '2.0.0b5', False),
    ('2.4.8.0', '<=', '2.0.0b5', False),
    ('2.4.8.1', '<=', '2.0.0b5', False),
    ('2.4.8b5', '<=', '2.0.0b5', False),
    ('2.4.8.post1', '<=', '2.0.0b5', False),
    ('2.0', '<=', '2.0.0b5', False),
    ('2', '<=', '2.0.0b5', False),
    ('2.0.0b5', '<=', '2.0.0b5', True),
    ('2.0.post1', '<=', '2.0.0b5', False),
    ('2.4.8', '<=', '2.0.post1', False),
    ('2.4.8.0', '<=', '2.0.post1', False),
    ('2.4.8.1', '<=', '2.0.post1', False),
    ('2.4.8b5', '<=', '2.0.post1', False),
    ('2.4.8.post1', '<=', '2.0.post1', False),
    ('2.0', '<=', '2.0.post1', True),
    ('2', '<=', '2.0.post1', True),
    ('2.0.0b5', '<=', '2.0.post1', True),
    ('2.0.post1', '<=', '2.0.post1', True),
    ('2.4.8', '<', '2.4.8', False),
    ('2.4.8.0', '<', '2.4.8', False),
    ('2.4.8.1', '<', '2.4.8', False),
    ('2.4.8b5', '<', '2.4.8', False),
    ('2.4.8.post1', '<', '2.4.8', False),
    ('2.0', '<', '2.4.8', True),
    ('2', '<', '2.4.8', True),
    ('2.0.0b5', '<', '2.4.8', True),
    ('2.0.post1', '<', '2.4.8', True),
    ('2.4.8', '<', '2.4.8.0', False),
    ('2.4.8.0', '<', '2.4.8.0', False),
    ('2.4.8.1', '<', '2.4.8.0', False),
    ('2.4.8b5', '<', '2.4.8.0', False),
    ('2.4.8.post1', '<', '2.4.8.0', False),
    ('2.0', '<', '2.4.8.0', True),
    ('2', '<', '2.4.8.0', True),
    ('2.0.0b5', '<', '2.4.8.0', True),
    ('2.0.post1', '<', '2.4.8.0', True),
    ('2.4.8', '<', '2.4.8.1', True),
    ('2.4.8.0', '<', '2.4.8.1', True),
    ('2.4.8.1', '<', '2.4.8.1', False),
    ('2.4.8b5', '<', '2.4.8.1', True),
    ('2.4.8.post1', '<', '2.4.8.1', True),
    ('2.0', '<', '2.4.8.1', True),
    ('2', '<', '2.4.8.1', True),
    ('2.0.0b5', '<', '2.4.8.1', True),
    ('2.0.post1', '<', '2.4.8.1', True),
    ('2.4.8', '<', '2.4.8.*', False),
    ('2.4.8.0', '<', '2.4.8.*', False),
    ('2.4.8.1', '<', '2.4.8.*', False),
    ('2.4.8b5', '<', '2.4.8.*', False),
    ('2.4.8.post1', '<', '2.4.8.*', False),
    ('2.0', '<', '2.4.8.*', True),
    ('2', '<', '2.4.8.*', True),
    ('2.0.0b5', '<', '2.4.8.*', True),
    ('2.0.post1', '<', '2.4.8.*', True),
    ('2.4.8', '<', '2.4.8b5', False),
    ('2.4.8.0', '<', '2.4.8b5', False),
    ('2.4.8.1', '<', '2.4.8b5', False),
    ('2.4.8b5', '<', '2.4.8b5', False),
    ('2.4.8.post1', '<', '2.4.8b5', False),
    ('2.0', '<', '2.4.8b5', True),
    ('2', '<', '2.4.8b5', True),
    ('2.0.0b5', '<', '2.4.8b5', True),
    ('2.0.post1', '<', '2.4.8b5', True),
    ('2.4.8', '<', '2.4.8.post1', True),
    ('2.4.8.0', '<', '2.4.8.post1', True),
    ('2.4.8.1', '<', '2.4.8.post1', False),
    ('2.4.8b5', '<', '2.4.8.post1', False),
    ('2.4.8.post1', '<', '2.4.8.post1', False),
    ('2.0', '<', '2.4.8.post1', True),
    ('2', '<', '2.4.8.post1', True),
    ('2.0.0b5', '<', '2.4.8.post1', True),
    ('2.0.post1', '<', '2.4.8.post1', True),
    ('2.4.8', '<', '2.0', False),
    ('2.4.8.0', '<', '2.0', False),
    ('2.4.8.1', '<', '2.0', False),
    ('2.4.8b5', '<', '2.0', False),
    ('2.4.8.post1', '<', '2.0', False),
    ('2.0', '<', '2.0', False),
    ('2', '<', '2.0', False),
    ('2.0.0b5', '<', '2.0', False),
    ('2.0.post1', '<', '2.0', False),
    ('2.4.8', '<', '2', False),
    ('2.4.8.0', '<', '2', False),
    ('2.4.8.1', '<', '2', False),
    ('2.4.8b5', '<', '2', False),
    ('2.4.8.post1', '<', '2', False),
    ('2.0', '<', '2', False),
    ('2', '<', '2', False),
    ('2.0.0b5', '<', '2', False),
    ('2.0.post1', '<', '2', False),
    ('2.4.8', '<', '2.*', False),
    ('2.4.8.0', '<', '2.*', False),
    ('2.4.8.1', '<', '2.*', False),
    ('2.4.8b5', '<', '2.*', False),
    ('2.4.8.post1', '<', '2.*', False),
    ('2.0', '<', '2.*', False),
    ('2', '<', '2.*', False),
    ('2.0.0b5', '<', '2.*', False),
    ('2.0.post1', '<', '2.*', False),
    ('2.4.8', '<', '2.0.0b5', False),
    ('2.4.8.0', '<', '2.0.0b5', False),
    ('2.4.8.1', '<', '2.0.0b5', False),
    ('2.4.8b5', '<', '2.0.0b5', False),
    ('2.4.8.post1', '<', '2.0.0b5', False),
    ('2.0', '<', '2.0.0b5', False),
    ('2', '<', '2.0.0b5', False),
    ('2.0.0b5', '<', '2.0.0b5', False),
    ('2.0.post1', '<', '2.0.0b5', False),
    ('2.4.8', '<', '2.0.post1', False),
    ('2.4.8.0', '<', '2.0.post1', False),
    ('2.4.8.1', '<', '2.0.post1', False),
    ('2.4.8b5', '<', '2.0.post1', False),
    ('2.4.8.post1', '<', '2.0.post1', False),
    ('2.0', '<', '2.0.post1', True),
    ('2', '<', '2.0.post1', True),
    ('2.0.0b5', '<', '2.0.post1', False),
    ('2.0.post1', '<', '2.0.post1', False),
    ('2.4.8', '>=', '2.4.8', True),
    ('2.4.8.0', '>=', '2.4.8', True),
    ('2.4.8.1', '>=', '2.4.8', True),
    ('2.4.8b5', '>=', '2.4.8', False),
    ('2.4.8.post1', '>=', '2.4.8', True),
    ('2.0', '>=', '2.4.8', False),
    ('2', '>=', '2.4.8', False),
    ('2.0.0b5', '>=', '2.4.8', False),
    ('2.0.post1', '>=', '2.4.8', False),
    ('2.4.8', '>=', '2.4.8.0', True),
    ('2.4.8.0', '>=', '2.4.8.0', True),
    ('2.4.8.1', '>=', '2.4.8.0', True),
    ('2.4.8b5', '>=', '2.4.8.0', False),
    ('2.4.8.post1', '>=', '2.4.8.0', True),
    ('2.0', '>=', '2.4.8.0', False),
    ('2', '>=', '2.4.8.0', False),
    ('2.0.0b5', '>=', '2.4.8.0', False),
    ('2.0.post1', '>=', '2.4.8.0', False),
    ('2.4.8', '>=', '2.4.8.1', False),
    ('2.4.8.0', '>=', '2.4.8.1', False),
    ('2.4.8.1', '>=', '2.4.8.1', True),
    ('2.4.8b5', '>=', '2.4.8.1', False),
    ('2.4.8.post1', '>=', '2.4.8.1', False),
    ('2.0', '>=', '2.4.8.1', False),
    ('2', '>=', '2.4.8.1', False),
    ('2.0.0b5', '>=', '2.4.8.1', False),
    ('2.0.post1', '>=', '2.4.8.1', False),
    ('2.4.8', '>=', '2.4.8.*', True),
    ('2.4.8.0', '>=', '2.4.8.*', True),
    ('2.4.8.1', '>=', '2.4.8.*', True),
    ('2.4.8b5', '>=', '2.4.8.*', True),
    ('2.4.8.post1', '>=', '2.4.8.*', True),
    ('2.0', '>=', '2.4.8.*', False),
    ('2', '>=', '2.4.8.*', False),
    ('2.0.0b5', '>=', '2.4.8.*', False),
    ('2.0.post1', '>=', '2.4.8.*', False),
    ('2.4.8', '>=', '2.4.8b5', True),
    ('2.4.8.0', '>=', '2.4.8b5', True),
    ('2.4.8.1', '>=', '2.4.8b5', True),
    ('2.4.8b5', '>=', '2.4.8b5', True),
    ('2.4.8.post1', '>=', '2.4.8b5', True),
    ('2.0', '>=', '2.4.8b5', False),
    ('2', '>=', '2.4.8b5', False),
    ('2.0.0b5', '>=', '2.4.8b5', False),
    ('2.0.post1', '>=', '2.4.8b5', False),
    ('2.4.8', '>=', '2.4.8.post1', False),
    ('2.4.8.0', '>=', '2.4.8.post1', False),
    ('2.4.8.1', '>=', '2.4.8.post1', True),
    ('2.4.8b5', '>=', '2.4.8.post1', False),
    ('2.4.8.post1', '>=', '2.4.8.post1', True),
    ('2.0', '>=', '2.4.8.post1', False),
    ('2', '>=', '2.4.8.post1', False),
    ('2.0.0b5', '>=', '2.4.8.post1', False),
    ('2.0.post1', '>=', '2.4.8.post1', False),
    ('2.4.8', '>=', '2.0', True),
    ('2.4.8.0', '>=', '2.0', True),
    ('2.4.8.1', '>=', '2.0', True),
    ('2.4.8b5', '>=', '2.0', True),
    ('2.4.8.post1', '>=', '2.0', True),
    ('2.0', '>=', '2.0', True),
    ('2', '>=', '2.0', True),
    ('2.0.0b5', '>=', '2.0', False),
    ('2.0.post1', '>=', '2.0', True),
    ('2.4.8', '>=', '2', True),
    ('2.4.8.0', '>=', '2', True),
    ('2.4.8.1', '>=', '2', True),
    ('2.4.8b5', '>=', '2', True),
    ('2.4.8.post1', '>=', '2', True),
    ('2.0', '>=', '2', True),
    ('2', '>=', '2', True),
    ('2.0.0b5', '>=', '2', False),
    ('2.0.post1', '>=', '2', True),
    ('2.4.8', '>=', '2.*', True),
    ('2.4.8.0', '>=', '2.*', True),
    ('2.4.8.1', '>=', '2.*', True),
    ('2.4.8b5', '>=', '2.*', True),
    ('2.4.8.post1', '>=', '2.*', True),
    ('2.0', '>=', '2.*', True),
    ('2', '>=', '2.*', True),
    ('2.0.0b5', '>=', '2.*', True),
    ('2.0.post1', '>=', '2.*', True),
    ('2.4.8', '>=', '2.0.0b5', True),
    ('2.4.8.0', '>=', '2.0.0b5', True),
    ('2.4.8.1', '>=', '2.0.0b5', True),
    ('2.4.8b5', '>=', '2.0.0b5', True),
    ('2.4.8.post1', '>=', '2.0.0b5', True),
    ('2.0', '>=', '2.0.0b5', True),
    ('2', '>=', '2.0.0b5', True),
    ('2.0.0b5', '>=', '2.0.0b5', True),
    ('2.0.post1', '>=', '2.0.0b5', True),
    ('2.4.8', '>=', '2.0.post1', True),
    ('2.4.8.0', '>=', '2.0.post1', True),
    ('2.4.8.1', '>=', '2.0.post1', True),
    ('2.4.8b5', '>=', '2.0.post1', True),
    ('2.4.8.post1', '>=', '2.0.post1', True),
    ('2.0', '>=', '2.0.post1', False),
    ('2', '>=', '2.0.post1', False),
    ('2.0.0b5', '>=', '2.0.post1', False),
    ('2.0.post1', '>=', '2.0.post1', True),
    ('2.4.8', '>', '2.4.8', False),
    ('2.4.8.0', '>', '2.4.8', False),
    ('2.4.8.1', '>', '2.4.8', True),
    ('2.4.8b5', '>', '2.4.8', False),
    ('2.4.8.post1', '>', '2.4.8', False),
    ('2.0', '>', '2.4.8', False),
    ('2', '>', '2.4.8', False),
    ('2.0.0b5', '>', '2.4.8', False),
    ('2.0.post1', '>', '2.4.8', False),
    ('2.4.8', '>', '2.4.8.0', False),
    ('2.4.8.0', '>', '2.4.8.0', False),
    ('2.4.8.1', '>', '2.4.8.0', True),
    ('2.4.8b5', '>', '2.4.8.0', False),
    ('2.4.8.post1', '>', '2.4.8.0', False),
    ('2.0', '>', '2.4.8.0', False),
    ('2', '>', '2.4.8.0', False),
    ('2.0.0b5', '>', '2.4.8.0', False),
    ('2.0.post1', '>', '2.4.8.0', False),
    ('2.4.8', '>', '2.4.8.1', False),
    ('2.4.8.0', '>', '2.4.8.1', False),
    ('2.4.8.1', '>', '2.4.8.1', False),
    ('2.4.8b5', '>', '2.4.8.1', False),
    ('2.4.8.post1', '>', '2.4.8.1', False),
    ('2.0', '>', '2.4.8.1', False),
    ('2', '>', '2.4.8.1', False),
    ('2.0.0b5', '>', '2.4.8.1', False),
    ('2.0.post1', '>', '2.4.8.1', False),
    ('2.4.8', '>', '2.4.8.*', True),
    ('2.4.8.0', '>', '2.4.8.*', True),
    ('2.4.8.1', '>', '2.4.8.*', True),
    ('2.4.8b5', '>', '2.4.8.*', True),
    ('2.4.8.post1', '>', '2.4.8.*', True),
    ('2.0', '>', '2.4.8.*', False),
    ('2', '>', '2.4.8.*', False),
    ('2.0.0b5', '>', '2.4.8.*', False),
    ('2.0.post1', '>', '2.4.8.*', False),
    ('2.4.8', '>', '2.4.8b5', True),
    ('2.4.8.0', '>', '2.4.8b5', True),
    ('2.4.8.1', '>', '2.4.8b5', True),
    ('2.4.8b5', '>', '2.4.8b5', False),
    ('2.4.8.post1', '>', '2.4.8b5', False),
    ('2.0', '>', '2.4.8b5', False),
    ('2', '>', '2.4.8b5', False),
    ('2.0.0b5', '>', '2.4.8b5', False),
    ('2.0.post1', '>', '2.4.8b5', False),
    ('2.4.8', '>', '2.4.8.post1', False),
    ('2.4.8.0', '>', '2.4.8.post1', False),
    ('2.4.8.1', '>', '2.4.8.post1', True),
    ('2.4.8b5', '>', '2.4.8.post1', False),
    ('2.4.8.post1', '>', '2.4.8.post1', False),
    ('2.0', '>', '2.4.8.post1', False),
    ('2', '>', '2.4.8.post1', False),
    ('2.0.0b5', '>', '2.4.8.post1', False),
    ('2.0.post1', '>', '2.4.8.post1', False),
    ('2.4.8', '>', '2.0', True),
    ('2.4.8.0', '>', '2.0', True),
    ('2.4.8.1', '>', '2.0', True),
    ('2.4.8b5', '>', '2.0', True),
    ('2.4.8.post1', '>', '2.0', True),
    ('2.0', '>', '2.0', False),
    ('2', '>', '2.0', False),
    ('2.0.0b5', '>', '2.0', False),
    ('2.0.post1', '>', '2.0', False),
    ('2.4.8', '>', '2', True),
    ('2.4.8.0', '>', '2', True),
    ('2.4.8.1', '>', '2', True),
    ('2.4.8b5', '>', '2', True),
    ('2.4.8.post1', '>', '2', True),
    ('2.0', '>', '2', False),
    ('2', '>', '2', False),
    ('2.0.0b5', '>', '2', False),
    ('2.0.post1', '>', '2', False),
    ('2.4.8', '>', '2.*', True),
    ('2.4.8.0', '>', '2.*', True),
    ('2.4.8.1', '>', '2.*', True),
    ('2.4.8b5', '>', '2.*', True),
    ('2.4.8.post1', '>', '2.*', True),
    ('2.0', '>', '2.*', True),
    ('2', '>', '2.*', True),
    ('2.0.0b5', '>', '2.*', True),
    ('2.0.post1', '>', '2.*', True),
    ('2.4.8', '>', '2.0.0b5', True),
    ('2.4.8.0', '>', '2.0.0b5', True),
    ('2.4.8.1', '>', '2.0.0b5', True),
    ('2.4.8b5', '>', '2.0.0b5', True),
    ('2.4.8.post1', '>', '2.0.0b5', True),
    ('2.0', '>', '2.0.0b5', True),
    ('2', '>', '2.0.0b5', True),
    ('2.0.0b5', '>', '2.0.0b5', False),
    ('2.0.post1', '>', '2.0.0b5', False),
    ('2.4.8', '>', '2.0.post1', True),
    ('2.4.8.0', '>', '2.0.post1', True),
    ('2.4.8.1', '>', '2.0.post1', True),
    ('2.4.8b5', '>', '2.0.post1', True),
    ('2.4.8.post1', '>', '2.0.post1', True),
    ('2.0', '>', '2.0.post1', False),
    ('2', '>', '2.0.post1', False),
    ('2.0.0b5', '>', '2.0.post1', False),
    ('2.0.post1', '>', '2.0.post1', False),
    ('1.dev1', '>', '1a1', False),
    ('1a1', '>', '1.dev1', True),
    ('1a1', '>', '1b1', False),
    ('1b1', '>', '1a1', True),
    ('1b1', '>', '1rc1', False),
    ('1', '>', '1rc1', True),
    ('1', '>', '1.post1', False),
    ('1.post1', '>', '1', False),
])
def test_requirement(version, op, arg, expected):
    assert (version in pkg_resources.Requirement.parse('foobar {} {}'.format(op, arg))) == expected
    # The section below will attempt further validation of accurate conversion using
    # rpmdev-vercmp.  However, that can only tell us that two versions are equal or
    # that one is greater than the other.  We can't test rich deps.
    requirement = convert('foobar', op, arg)
    if op == '===':
        # We treat '===' as '==', which is not entirely the same behavior
        return
    if requirement[0] == '(':
        # ~= and != will produce rich deps, which we can't currently test.
        return

    ver_a = RpmVersion(version)
    rpm_op, ver_b = requirement.split(' ')[1:3]

    # There are some minor incompatibilities resulting from these converted
    # requirement expressions.  In these cases, the test will "return" because
    # we know that we produce different results.

    if ver_a.post and not 'post' in ver_b and rpm_op == '>':
        # "post" versions in Python must be treated as greater than the same version
        # lacking a post component, but they must not satisfy a ">" requirement
        # unless the requirement also has a post component.
        #
        # >>> '2.0.post1' in pkg_resources.Requirement.parse('foo>2')
        # False
        #
        # This produces strange results in some corner cases:
        #
        # >>> '2.0' in pkg_resources.Requirement.parse('foo>2.0b5')
        # True
        # >>> '2.0.post1' in pkg_resources.Requirement.parse('foo>2.0b5')
        # False
        #
        # One option is that rpm packages should not specify the post
        # component in the Version field.  However, that would also
        # create differences with the distutils == operator:
        #
        # >>> '2.0.post1' in pkg_resources.Requirement.parse('foo==2.0')
        # False
        return

    if ver_a.pre and 'post' in ver_b and rpm_op == '<':
        # rpm will match this behavior:
        #
        # >>> '2.0' in pkg_resources.Requirement.parse('foo<2.0.post1')
        # True
        #
        # but not this:
        #
        # >>> '2.0b5' in pkg_resources.Requirement.parse('foo<2.0.post1')
        # False
        return

    if ver_a.pre and '>' in rpm_op and '.*' in arg:
        # distutils will allow a prerelease to match both '>' and '>='
        # when used with prefix matching.
        # The use of prefix matching in conjunction with ordered comparison
        # is undefined behavior in distutils.
        #
        # >>> '2.0b5' in pkg_resources.Requirement.parse('foo>2.*')
        # True
        # >>> '2.0b5' in pkg_resources.Requirement.parse('foo>2')
        # False
        ver_a.pre = None

    vercmp = subprocess.run(['rpmdev-vercmp', str(ver_a), str(ver_b)])
    if rpm_op == '=':
        assert (vercmp.returncode == 0) == expected
    if rpm_op == '>=':
        assert (vercmp.returncode in [0, 11]) == expected
    if rpm_op == '>':
        assert (vercmp.returncode == 11) == expected
    if rpm_op == '<=':
        assert (vercmp.returncode in [0, 12]) == expected
    if rpm_op == '<':
        assert (vercmp.returncode == 12) == expected
