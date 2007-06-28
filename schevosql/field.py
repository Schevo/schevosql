"""Schevo field SQL operations.

For copyright, license, and warranty, see bottom of file.
"""

from dispatch import generic

from schevo.constant import UNASSIGNED
from schevo import field as F


[generic()]
def to_colspec(dialect, field):
    """Return a tuple of (specs, constraints) for the field."""


[generic()]
def to_data(dialect, field):
    """Return a tuple of (col name, value) suitable for INSERT."""


# --------------------------------------------------------------------


[to_colspec.when("dialect == 'jet' and isinstance(field, F.Field)")]
def to_colspec(dialect, field):
    if field.max_size is not None:
        max_size = '(%i)' % field.max_size
    else:
        max_size = ''
    specs = [
        '`{table}_%s` TEXT %s %s' % (field._attribute,
                                     max_size,
                                     ('', ' NOT NULL')[field.required],
                                     ),
        ]
    constraints = []
    return (specs, constraints)


[to_colspec.when("dialect == 'jet' and isinstance(field, F.Integer)")]
def to_colspec(dialect, field):
    specs = [
        '`{table}_%s` INTEGER %s' % (field._attribute,
                                     ('', ' NOT NULL')[field.required],
                                     ),
        ]
    constraints = []
    return (specs, constraints)


[to_colspec.when("dialect == 'jet' and isinstance(field, F.Float)")]
def to_colspec(dialect, field):
    specs = [
        '`{table}_%s` FLOAT %s' % (field._attribute,
                                   ('', ' NOT NULL')[field.required],
                                   ),
        ]
    constraints = []
    return (specs, constraints)


[to_colspec.when("dialect == 'jet' and isinstance(field, F.Money)")]
def to_colspec(dialect, field):
    # XXX: Should really be a DECIMAL type.
    specs = [
        '`{table}_%s` FLOAT %s' % (field._attribute,
                                   ('', ' NOT NULL')[field.required],
                                   ),
        ]
    constraints = []
    return (specs, constraints)


[to_colspec.when("dialect == 'jet' and isinstance(field, F.Boolean)")]
def to_colspec(dialect, field):
    specs = [
        '`{table}_%s` BIT %s' % (field._attribute,
                                 ('', ' NOT NULL')[field.required],
                                 ),
        ]
    constraints = []
    return (specs, constraints)


[to_colspec.when("dialect == 'jet' and isinstance(field, F.Entity)")]
def to_colspec(dialect, field):
    specs = []
    constraints = []
    for class_name in field.allow:
        col_name = '{table}_%s' % field._attribute
        if len(field.allow) > 1:
            col_name += '_%s' % class_name
        specs.append('`%s` INTEGER' % col_name)
        constraints.append(
            'ALTER TABLE `{table}` '
            'ADD FOREIGN KEY (`%s`) '
            'REFERENCES %s (`%s_oid`);\n' %
            (col_name, class_name, class_name)
            )
    return (specs, constraints)


# --------------------------------------------------------------------


[generic()]
def to_data(dialect, field):
    """Return a tuple of (col name, value) suitable for INSERT."""


[to_data.when("dialect == 'jet' and isinstance(field, F.Field)")]
def to_data(dialect, field):
    if field._value is not UNASSIGNED:
        col_name = '`{table}_%s`' % field._attribute
        value = '"%s"' % str(field).replace('"', '""')
        return (col_name, value)


[to_data.when("dialect == 'jet' and isinstance(field, F.Integer)")]
def to_data(dialect, field):
    if field._value is not UNASSIGNED:
        col_name = '`{table}_%s`' % field._attribute
        value = '%i' % field._value
        return (col_name, value)


[to_data.when("dialect == 'jet' and isinstance(field, F.Float)")]
def to_data(dialect, field):
    if field._value is not UNASSIGNED:
        col_name = '`{table}_%s`' % field._attribute
        value = '%f' % field._value
        return (col_name, value)


[to_data.when("dialect == 'jet' and isinstance(field, F.Money)")]
def to_data(dialect, field):
    if field._value is not UNASSIGNED:
        col_name = '`{table}_%s`' % field._attribute
        value = '%f' % field._value
        return (col_name, value)


[to_data.when("dialect == 'jet' and isinstance(field, F.Boolean)")]
def to_data(dialect, field):
    if field._value is not UNASSIGNED:
        col_name = '`{table}_%s`' % field._attribute
        value = '%i' % field._value
        return (col_name, value)


[to_data.when("dialect == 'jet' and isinstance(field, F.Entity)")]
def to_data(dialect, field):
    if field._value is not UNASSIGNED:
        class_name = field._value.__class__.__name__
        col_name = field._attribute
        if len(field.allow) > 1:
            col_name += '_%s' % class_name
        col_name = '`{table}_%s`' % col_name
        value = '%i' % field._value.sys.oid
        return (col_name, value)


# Copyright (C) 2001-2005 Orbtech, L.L.C.
#
# Schevo
# http://schevo.org/
#
# Orbtech
# Saint Louis, MO
# http://orbtech.com/
#
# This toolkit is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This toolkit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
