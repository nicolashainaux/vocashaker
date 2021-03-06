# -*- coding: utf-8 -*-

# Memini is a simple project that creates vocabulary grids to train.
# Copyright 2019 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Memini.

# Memini is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Memini is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Memini; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sqlite3

from click.testing import CliRunner

from memini.core.prefs import DEFAULT_Q_NB
from memini.core.env import TEST_DB_PATH
from memini import run, list_, parse, delete, remove, create, add, show
from memini import rename, generate, edit, duplicate, dump, sort, update
from memini import merge


class TDBManager:
    """
    Simple CM for the test database. Rolls back AND closes everything at exit.

    The testdb fixture defined in conftest.py cannot be used because every
    command in main script needs to set shared.db. This TDBManager is
    intended to be used as a mock to replace the real user db.
    """
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(TEST_DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute('SAVEPOINT starttest;')
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.execute('ROLLBACK TO SAVEPOINT starttest;')
        self.conn.close()


def test_run():
    runner = CliRunner()
    result = runner.invoke(run, [])
    assert result.exit_code == 0


def test_list_(mocker):
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(list_, ['tables'])
    assert result.output == 'table1\ntable2\n'
    assert result.exit_code == 0
    result = runner.invoke(list_, ['stuff'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1


def test_parse(mocker, fs):
    fs.create_file('empty_file.txt')
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(parse, ['empty_file.txt', '<Latin>:<Français>'])
    assert result.output.startswith('Warning: ')
    assert result.exit_code == 0


def test_delete(mocker):
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(delete, ['table3'])
    assert result.exit_code == 1
    assert result.output.startswith('Error: ')


def test_remove(mocker):
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(remove, ['table3', '1-4'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1


def test_create(mocker, fs):
    fs.create_file('empty_file.txt')
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(create, ['table1', 'empty_file.txt',
                                    '<Latin>:<Français>'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1


def test_add(mocker, fs):
    fs.create_file('empty_file.txt')
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(add, ['table3', 'empty_file.txt',
                                 '<Latin>:<Français>'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1


def test_show(mocker):
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(show, ['table3'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1
    result = runner.invoke(show, ['table1', '--sort', '2'])
    assert result.output == \
        ' id |        col1       |   col2  \n'\
        '----+-------------------+---------\n'\
        '  1 | adventus,  us, m. | arrivée \n'\
        '  3 |  candidus,  a, um |  blanc  \n'\
        '  2 |    aqua , ae, f   |   eau   \n'\
        '  4 |   sol, solis, m   |  soleil \n'


def test_sort(mocker):
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(sort, ['table3'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1


def test_update(mocker):
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(update, ['table3', '1 | a | b | c'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1


def test_dump(mocker):
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(dump, ['0'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1


def test_rename(mocker):
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(rename, ['table1', 'table2'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1


def test_merge(mocker):
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(merge, ['table1', 'table2'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1


def test_duplicate(mocker):
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(duplicate, ['table1', 'table2'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1


def test_edit(mocker):
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(edit, ['table3'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1


def test_generate(mocker, fs):
    mocker.patch('memini.core.database.Manager', return_value=TDBManager())
    runner = CliRunner()
    result = runner.invoke(generate, ['table3'])
    assert result.output.startswith('Error: ')
    assert result.exit_code == 1

    fs.create_file('exists.txt')
    mocker.patch('memini.core.terminal.ask_yes_no', return_value=False)
    result = runner.invoke(generate, ['table1', '-n 3', '--output=exists.txt'])
    assert result.output.startswith('Info: ')
    assert result.exit_code == 0

    result = runner.invoke(generate, [])
    assert result.output.startswith('Error: Missing argument \'NAME\'. It is '
                                    'required unless')
    assert result.exit_code == 1

    mg = mocker.patch('memini.core.commands.generate')
    result = runner.invoke(generate, ['--use-previous'])
    mg.assert_called_with('1', nb=DEFAULT_Q_NB, scheme=None,
                          output=None, force=False, tpl=None,
                          edit=True, use_previous=True)
    assert result.exit_code == 0
