# -*- encoding: utf-8 -*-
import gtk
import gtk.glade
import goocanvas

import dialogs
import model
import box

from window import Window

class Main(Window):
    """ 
    Ventana Principal del programa
    """
    
    # Almacena la posicion en donde se hizo clic derecho.
    # Stores the position where right clic was pressed.

    x_position = 0
    y_position = 0

    def __init__(self):
        Window.__init__(self, 'main.glade')
        self.view.main.show()
        self._create_canvas()

    # Construye el widget canvas.
    # This builds the canvas widget.

    def _create_canvas(self):
        self.view.canvas = goocanvas.Canvas()
        self.view.canvas.props.x2 = 600
        self.view.canvas.props.y2 = 400
        self.view.scroll.add(self.view.canvas)
        self.view.canvas.show()
        self.view.canvas.connect('event', self.on_event)

    # Al presionar clic derecho sobre el canvas desplegamos el menu de opciones y actualizamos la posicion del mouse.
    # When right clic is pressed over the canvas we raise the options menu and update the coordinates.

    def on_event(self, widget, event):
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            self.view.popup.popup(None, None, None, event.button, event.time)
            self.x_position = event.x
            self.y_position = event.y

    def on_quit_item__activate(self, widget):
        self.on_main__destroy(widget)

    def on_main__destroy(self, widget):
        gtk.main_quit()

    # Al presionar sobre el boton 'Add' del menu desplegamos la ventana para crear una nueva clase.
    # When the 'Add' button is pressed we raise the window to create a new class.

    def on_add__activate(self, widget):
        new_model = model.Model()
        new_dialog = dialogs.classview.ClassView(new_model)
        dialog_ret_val = new_dialog.view.dialog1.run()

        # Si alguien sabe como averiguar si se presiono OK o CANCEL...
        # En caso que se presione CANCEL, no hay que dibujar nada...

        if dialog_ret_val == 1:
            root = self.view.canvas.get_root_item()
            box1 = box.Box(self.x_position, self.y_position, new_model, root)
            box1.group.connect('button_press_event',
                    self.on_button_press_event, box1)

    def on_button_press_event(self, widget, event, extra, box):
        print "Se activa un evento:", event 
        box.model.show()

if __name__ == '__main__':
    main = Main()
    gtk.main()