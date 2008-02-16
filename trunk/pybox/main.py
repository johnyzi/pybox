# -*- encoding: utf-8 -*-
import gtk
import gtk.glade
import goocanvas

import common
import dialogs
import model
import canvas

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

    def on_quit_item__activate(self, widget):
        self.on_main__destroy(widget)

    def on_main__destroy(self, widget):
        gtk.main_quit()

    def on_aboutitem__activate(self, item):
        image = gtk.Image()
        dialog = gtk.AboutDialog()
        dialog.set_name("Pybox")
        dialog.set_comments("A simple class diagram tool.")
        dialog.set_license(common.GPL_TEXT)
        dialog.set_authors(['a', 'b'])
        image.set_from_file("../pixmaps/logo.png")
        dialog.set_logo(image.get_pixbuf())
        dialog.run()
        dialog.hide()


if __name__ == '__main__':
    main = Main()
    gtk.main()
