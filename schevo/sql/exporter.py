"""SQL exporter for Schevo databases.

For copyright, license, and warranty, see bottom of file.
"""

__svn__ = "$Id$"
__rev__ = "$Rev$"[6:-2]

from schevo.constant import UNASSIGNED
from schevo.sql.field import to_colspec, to_data


class Exporter(object):
    """Exports a Schevo root to a pickle stream."""

    def __init__(self, db, dialect='jet'):
        """Create an exporter instance.

        - `db`: An open Schevo database.
        - `dialect`: Currently, only 'jet' is supported.  In the future,
          'mysql', 'postgres', etc. may be supported.
        """
        self.db = db
        self.dialect = dialect

    def export_to(self, output, schema=True, data=True, drop_tables=False):
        """Uses export_gen to do a blocking export of an entire
        database."""
        for x in self.export_gen(output, schema, data, drop_tables):
            pass

    def export_gen(self, output, schema=True, data=True, drop_tables=False):
        """Export to file-like object, yielding tuples of integers
        (current_extent, total_extents) after each extent is exported.

        - `schema`: True if schema should be exported.
        - `data`: True if data should be exported.
        - `drop_tables`: True if 'DROP TABLE' statements should be written
           before 'CREATE TABLE' statements.
        """
        db = self.db
        dialect = self.dialect
        constraints = []
        extent_names = db.extent_names()
        processed = 0
        total = len(extent_names)
        for extent_name in extent_names:
            # XXX: For now, skip icons.
            if extent_name == 'SchevoIcon':
                continue
            extent = db.extent(extent_name)
            if schema:
                EntityClass = extent._EntityClass
                if drop_tables:
                    statement = 'DROP TABLE `%s`;\n' % extent_name
                    output.write(statement)
                statements = ['CREATE TABLE `%s` (' % extent_name]
                col_parts = ['%s_oid INTEGER' % extent_name,
                            '%s_rev INTEGER' % extent_name,
                            ]
                for f_name, FieldClass in EntityClass._field_spec.iteritems():
                    field = FieldClass(None, f_name)
                    if not field.readonly and field.fget is None:
                        specs, constrs = to_colspec(dialect, field)
                        constrs = [c.replace('{table}', extent_name)
                                   for c in constrs]
                        specs = [s.replace('{table}', extent_name)
                                 for s in specs]
                        col_parts.extend(specs)
                        constraints.extend(constrs)
                col_parts.append('PRIMARY KEY (`%s_oid`)' % extent_name)
                statements.append(', '.join(col_parts))
                statements.append(');\n')
                statement = ''.join(statements)
                output.write(statement)
            if data:
                for entity in extent.find():
                    col_names = ['`%s_oid`' % extent_name,
                                 '`%s_rev`' % extent_name,
                                 ]
                    col_values = [str(entity.sys.oid),
                                  str(entity.sys.rev),
                                  ]
                    for field_name, field in entity.sys.fields(
                        include_readonly_fget=False,
                        ).iteritems():
                        if field._value is not UNASSIGNED:
                            data = to_data(dialect, field)
                            if data is not None:
                                col_name, col_value = data
                                col_name = col_name.replace(
                                    '{table}', extent_name)
                                col_names.append(col_name)
                                col_values.append(col_value)
                    statement = 'INSERT INTO %s (%s) VALUES (%s);\n' % (
                        extent_name,
                        ', '.join(col_names),
                        ', '.join(col_values),
                        )
                    output.write(statement)
            processed += 1
            yield (processed, total)
        for constr in constraints:
            output.write(constr)


# Copyright (C) 2001-2005 Orbtech, L.L.C.
#
# Schevo
# http://schevo.org/
#
# Orbtech
# 709 East Jackson Road
# Saint Louis, MO  63119-4241
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
