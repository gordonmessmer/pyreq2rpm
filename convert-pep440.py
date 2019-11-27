#!/usr/bin/env python3

# convert-pep440 - translates python packaging requirements into rpm
# Copyright (C) 2019  Gordon Messmer <gordon.messmer@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from pkg_resources import parse_version

version_ids = ('2.4.8', '2.4.8.0', '2.4.8.1', '2.4.8.*', '2.0', '2', '2.*')

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
