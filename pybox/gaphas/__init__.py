"""
Gaphas 
======

Gaphor's Canvas.

This module contains the application independant parts of Gaphor's Canvas.
It can and may be used by others under the terms of the GNU LGPL licence.
"""

__version__ = "$Revision: 1130 $"
# $HeadURL: http://svn.devjavu.com/gaphor/gaphas/tags/gaphas-0.3.6/gaphas/__init__.py $

from canvas import Canvas
from item import Item, Line, Element, Handle
from view import View, GtkView

