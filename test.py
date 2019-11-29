#!/usr/bin/env python3

from pkg_resources import Requirement
from pyreq2rpm import pyreq2rpm

VERSION_IDS = ('2.4.8', '2.4.8.0', '2.4.8.1', '2.4.8.*', '2.0', '2', '2.*',
               '2.4.8b5', '2.0.0b5', '2.4.8.post1', '2.0.post1')

name = 'foobar'
for x in pyreq2rpm.OPERATORS.keys():
    for y in VERSION_IDS:
        try:
            Requirement('%s %s %s' % (name, x, y))
        except:
            print('%s %s %s is invalid in Requirements' % (name, x, y))
        print('%s %s : %s' % (x, y, pyreq2rpm.convert(name, x, y)))
