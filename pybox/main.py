# -*- encoding: utf-8 -*-
import gtk
import gtk.glade
import goocanvas

from window import Window

class Main(Window):
    """ 
    Ventana Principal del programa
    """
    
    def __init__(self):
        Window.__init__(self, 'main.glade')
        self.view.main.show()
        self._create_canvas()

    def _create_canvas(self):
        self.view.canvas = goocanvas.Canvas()
        self.view.eventbox.add(self.view.canvas)
        self.view.canvas.show()
        self.view.canvas.connect('event', self.on_event)

    def on_event(self, widget, event):
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            self.view.popup.popup(None, None, None, event.button, event.time)

    def on_quit_item__activate(self, widget):
        self.on_main__destroy(widget)

    def on_main__destroy(self, widget):
        gtk.main_quit()
    
if __name__ == '__main__':
    main = Main()
    gtk.main()
