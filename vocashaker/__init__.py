# -*- coding: utf-8 -*-

# VocaShaker is a simple project that creates vocabulary grids to train.
# Copyright 2019 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of VocaShaker.

# VocaShaker is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# VocaShaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with VocaShaker; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import click
import blessed

from vocashaker.core.env import USER_DB_PATH
from vocashaker.core.errors import CommandError, EmptyFileError
from vocashaker.core import shared
from vocashaker.core import database
from vocashaker.core import commands


shared.init()

__all__ = ['run']


@click.group()
def run():
    pass


@run.command('list')
@click.argument('what')
def list_(what):
    with database.Manager(USER_DB_PATH) as db:
        shared.db = db
        try:
            commands.list_(what)
        except CommandError as e:
            click.echo(str(e))


@run.command('parse')
@click.option('--errors-only', is_flag=True, default=False, show_default=True)
@click.argument('filename', type=click.Path(exists=True))
@click.argument('pattern')
def parse(filename, pattern, errors_only):
    with database.Manager(USER_DB_PATH) as db:
        shared.db = db
        try:
            commands.parse(filename, pattern, errors_only)
        except EmptyFileError as e:
            term = blessed.Terminal()
            click.echo(term.darkorange('Warning: ') + str(e))
