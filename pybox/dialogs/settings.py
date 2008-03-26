# -*- encoding: utf-8 -*-
import gtk
import gtk.glade
from window import Window

class Settings(Window):

    def __init__(self):
        Window.__init__(self, 'settings.glade')

    def run(self):
        self.view.settings.run()
