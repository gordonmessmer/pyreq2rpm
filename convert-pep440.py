#!/usr/bin/env python3

# Copyright 2019 pyproject-rpm-macros contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pkg_resources import parse_version, Requirement

version_ids = ('2.4.8', '2.4.8.0', '2.4.8.1', '2.4.8.*', '2.0', '2', '2.*',
               '2.4.8b5', '2.0.0b5', '2.4.8.post1', '2.0.post1')

class RpmVersion():
    def __init__(self, version_id):
        version = parse_version(version_id)
        if isinstance(version._version, str):
            self.version = version._version
        else:
            self.epoch = version._version.epoch
            self.version = list(version._version.release)
            self.pre = version._version.pre
            self.dev = version._version.dev
            self.post = version._version.post

    def increment(self):
        self.version[-1] += 1
        self.pre = None
        self.dev = None
        self.post = None
        return self

    def __str__(self):
        if isinstance(self.version, str):
            return self.version
        if self.epoch:
            rpm_epoch = str(self.epoch) + ':'
        else:
            rpm_epoch = ''
        while self.version[-1] == 0:
            self.version.pop()
        rpm_version = '.'.join(str(x) for x in self.version)
        if self.pre:
            rpm_suffix = '~%s' % ''.join(str(x) for x in self.pre)
        elif self.post:
            rpm_suffix = '^post%d' % self.post[1]
        else:
            rpm_suffix = ''
        return '%s%s%s' % (rpm_epoch, rpm_version, rpm_suffix)

def convert_compatible(name, operator, version_id):
    if version_id.endswith('.*'):
        return 'Invalid version'
    version = RpmVersion(version_id)
    if len(version.version) == 1:
        return 'Invalid version'
    upper_version = RpmVersion(version_id)
    upper_version.version.pop()
    upper_version.increment()
    return '(%s >= %s with %s < %s)' % (
        name, version, name, upper_version)

def convert_equal(name, operator, version_id):
    if version_id.endswith('.*'):
        version_id = version_id[:-2] + '.0'
        return convert_compatible(name, '~=', version_id)
    version = RpmVersion(version_id)
    return '%s = %s' % (name, version)

def convert_not_equal(name, operator, version_id):
    if version_id.endswith('.*'):
        version_id = version_id[:-2]
        version = RpmVersion(version_id)
        lower_version = RpmVersion(version_id).increment()
    else:
        version = RpmVersion(version_id)
        lower_version = version
    return '(%s < %s or %s > %s)' % (
        name, version, name, lower_version)

def convert_ordered(name, operator, version_id):
    if version_id.endswith('.*'):
        version_id = version_id[:-2]
        version = RpmVersion(version_id)
        if '>' == operator:
            operator = '>='
            version.increment()
    else:
        version = RpmVersion(version_id)
    return '%s %s %s' % (name, operator, version)

operators = {'~=': convert_compatible,
             '==': convert_equal,
             '!=': convert_not_equal,
             '<=': convert_ordered,
             '<':  convert_ordered,
             '>=': convert_ordered,
             '>':  convert_ordered}

name = 'foobar'
for x in operators.keys():
    for y in version_ids:
        try:
            Requirement('%s %s %s' % (name, x, y))
        except:
            print('%s %s %s is invalid in Requirements' % (name, x, y))
        print('%s %s : %s' % (x, y, operators[x](name, x, y)))
