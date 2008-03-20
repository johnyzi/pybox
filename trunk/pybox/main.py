# -*- encoding: utf-8 -*-
import gtk
import gtk.glade
import goocanvas

import common
import dialogs
import model
import canvas
import status
import dialogs.save
import config

from window import Window

class Main(Window):
    """ 
    Ventana Principal del programa
    """
    
    def __init__(self):
        Window.__init__(self, 'main.glade')
        self._create_canvas()
        self._create_status_bar()
        self.view.main.show()

    def set_title(self, string):
        self.view.main.set_title(string)

    def set_can_save(self, state):
        self.view.saveas.set_sensitive(state)
        self.view.new.set_sensitive(state)
        self.view.newbutton.set_sensitive(state)

    def set_can_export(self, state):
        self.view.export_png_item.set_sensitive(state)
        self.view.export_pdf_item.set_sensitive(state)

    def _create_canvas(self):
        self.canvas = canvas.Canvas(self)
        self.view.scroll.add(self.canvas)

    def _create_status_bar(self):
        self.view.status = status.StatusBar(self)
        self.view.status_placeholder.add(self.view.status)
        self.view.status.info("Starting program")

    def on_newbutton__clicked(self, widget):
        self.on_new__activate(widget)
    
    def on_new__activate(self, widget):
        self.canvas.new()

    def on_quit_item__activate(self, widget):
        self.on_main__delete_event(widget)

    def on_main__delete_event(self, widget, extra=None):
        if not config.DEBUG:
            return not self.canvas.new()

    def on_main__destroy(self, widget):
        gtk.main_quit()

    def on_export_png_item__activate(self, widget):
        dialogs.save.PNG(self.view.main, self.canvas, self.view.status)

    def on_export_pdf_item__activate(self, widget):
        dialogs.save.PDF(self.view.main, self.canvas, self.view.status)

    def on_saveas__activate(self, widget):
        self.canvas.save_as()

    def on_open__activate(self, widget):
        dialogs.open.Document(self.view.main, self.canvas, self.view.status)

    def on_aboutitem__activate(self, item):
        dialog = dialogs.about.About()
        self.view.status.info("Showing about dialog")
        dialog.run()
        self.view.status.info("About dialog has closed")

if __name__ == '__main__':
    main = Main()
    gtk.main()
