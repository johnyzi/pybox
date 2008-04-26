# -*- encoding: utf-8 -*-
import gtk
import gtk.glade
from window import Window

class Settings(Window):

    def __init__(self):
        Window.__init__(self, 'settings.glade')
        self.view.image2.set_from_file('../pixmaps/classic.png')
        self.view.image3.set_from_file('../pixmaps/round.png')

    def on_ok__clicked(self, widget, extra=None):
        self.view.settings.hide()
        
    def on_cancel__clicked(self, widget, extra=None):
        self.view.settings.hide()

    def run(self):
        self.view.settings.run()
