#!/usr/bin/env python3

# Copyright 2019 Gordon Messmer <gordon.messmer@gmail.com>
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

from pkg_resources import parse_version

version_ids = ('2.4.8', '2.4.8.0', '2.4.8.1', '2.4.8.*', '2.0', '2', '2.*',
               '2.4.8b5')

def strip_zeros(version_id):
    while version_id.endswith('.0'):
        version_id = version_id[:-2]
    return version_id

def increment_minor(version_id):
    next_ver = parse_version(version_id).base_version.split('.')
    # Increment the least significant number
    next_ver[-1] = str(int(next_ver[-1]) + 1)
    return '.'.join(next_ver)

def convert_compatible(name, operator, version_id):
    if version_id.endswith('.*'):
        return 'Invalid version'
    upper_id = parse_version(version_id).base_version.split('.')
    if len(upper_id) == 1:
        return 'Invalid version'
    upper_id = increment_minor('.'.join(upper_id[:-1]))
    return '(%s >= %s with %s < %s)' % (
        name, strip_zeros(version_id), name, strip_zeros(upper_id))

def convert_equal(name, operator, version_id):
    if version_id.endswith('.*'):
        version_id = version_id[:-2] + '.0'
        return convert_compatible(name, '~=', version_id)
    return '%s = %s' % (name, strip_zeros(version_id))

def convert_not_equal(name, operator, version_id):
    lower_id = version_id
    if version_id.endswith('.*'):
        version_id = version_id[:-2]
        lower_id = increment_minor(version_id)
    return '(%s < %s or %s > %s)' % (
        name, strip_zeros(version_id), name, strip_zeros(lower_id))

def convert_ordered(name, operator, version_id):
    return '%s %s %s' % (name, operator, strip_zeros(version_id))

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
        print('%s %s : %s' % (x, y, operators[x](name, x, y)))
