# -*- encoding: utf-8 -*-
import os
from config import Config

config = Config()

GPL_TEXT = \
"""This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

AUTHORS = [
    'Hugo Ruscitti <hugoruscitti@gmail.com>',
    'Lucas Liendo <mindmaster@gmail.com>',
    'Sergio Montañez <ser52g@gmail.com>',
    'Adrián Fernando Fiore <krashx0@hotmail.com>',]

def list_to_string(list):
    """Convert a list of classes to a unique string.

    ie: ['Man', 'Owner'] -> "Man, Owner"
    """
    return reduce(lambda a, b: "%s, %s" %(a, b), list)

def string_to_list(string):
    """Convert a strings of classes to a list of classes.

    ie: "Man, Owner" -> ['Man', 'Owner']
    """
    return string.split(', ')

def get_filename_without_extension(filename):
    name = os.path.basename(filename)
    return os.path.splitext(name)[0]

if __name__ == '__main__':
    print string_to_list("Man, Owner")
    print list_to_string(['Man', 'Owner', 'b', 'c'])
    print list_to_string(['Man'])
    print list_to_string(['<None>'])
