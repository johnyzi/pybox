# -*- encoding: utf-8 -*-
import gtk
import gtk.glade
import goocanvas

import common
import dialogs
import model
import canvas
import status

from window import Window

class Main(Window):
    """ 
    Ventana Principal del programa
    """
    
    def __init__(self):
        Window.__init__(self, 'main.glade')
        self.view.main.show()
        self.canvas = canvas.Canvas(self)
        self.view.scroll.add(self.canvas)
        self.view.status = status.StatusBar()
        self.view.status_placeholder.add(self.view.status)
        self.view.status.info("Starting program")

    def on_quit_item__activate(self, widget):
        self.on_main__destroy(widget)

    def on_main__destroy(self, widget):
        gtk.main_quit()

    def on_aboutitem__activate(self, item):
        dialog = dialogs.about.About()
        self.view.status.info("Showing about dialog")
        dialog.run()
        self.view.status.info("About dialog has closed")

if __name__ == '__main__':
    main = Main()
    gtk.main()
