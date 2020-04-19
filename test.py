#!/usr/bin/env python3

import subprocess
from pkg_resources import Requirement
from pyreq2rpm import pyreq2rpm

VERSION_IDS = ('2.4.8', '2.4.8.0', '2.4.8.1', '2.4.8.*', '2.0', '2', '2.*',
               '2.4.8b5', '2.0.0b5', '2.4.8.post1', '2.0.post1', '0.0')

def test_rpmbuild(dep):
    e = subprocess.run(['rpmbuild', '--nobuild', '--define',
                        'dep_test {}'.format(dep),
                        'tests/data/dep.spec'],)
    return e.returncode

name = 'foobar'
for x in pyreq2rpm.OPERATORS:
    for y in VERSION_IDS:
        try:
            Requirement('%s %s %s' % (name, x, y))
        except:
            print('%s %s %s is invalid in Requirements' % (name, x, y))
        print('%s %s : %s' % (x, y, pyreq2rpm.convert(name, x, y)))
        print(test_rpmbuild(pyreq2rpm.convert(name, x, y)))

print(pyreq2rpm.convert_requirement('pyparsing>=2.0.1,!=2.0.4,!=2.1.2,!=2.1.6'))
print(test_rpmbuild(pyreq2rpm.convert_requirement('pyparsing>=2.0.1,!=2.0.4,!=2.1.2,!=2.1.6')))
print(pyreq2rpm.convert_requirement('babel>=1.3,!=2.0'))
print(test_rpmbuild(pyreq2rpm.convert_requirement('babel>=1.3,!=2.0')))
