# -*- encoding: utf-8 -*-
import goocanvas
import box
import gtk
import popup

class Canvas(goocanvas.Canvas):

    # Almacena la posicion en donde se hizo clic derecho.
    # Stores the position where right clic was pressed.

    x_position = 0
    y_position = 0

    def __init__(self, main):
        goocanvas.Canvas.__init__(self)
        self.main = main
        self.classes = []

        # Construye el widget canvas.
        # This builds the canvas widget.

        self.props.x2 = 600
        self.props.y2 = 400
        self.show()
        self.connect('event', self.on_event)

        self.popup = popup.Popup(self)

    # Al presionar clic derecho sobre el canvas desplegamos el menu de opciones y actualizamos la posicion del mouse.
    # When right clic is pressed over the canvas we raise the options menu and update the coordinates.

    def on_event(self, widget, event):
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:

            # Si se presionó sobre el canvas habilitamos solamente la opcion Add.

            self.popup.show(event, new=True)

            
            self.x_position = event.x
            self.y_position = event.y

    def create_box(self, new_model):
        root = self.get_root_item()
        box1 = box.Box(self.x_position, self.y_position, new_model, root)
        box1.group.connect('button_press_event', self.on_button_press_event, box1)
        self.classes.append(new_model)

    def on_button_press_event(self, group, widget, event, box):
        '''print "Se activa un evento:", event 
        box.model.show()'''

        # Habilitamos la opciones Edit y Remove.


        # Almacenamos el box y el grupo para que pueda ser accedido por el
        # evento on_remove__activate o on_edit__activate.
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            print 'Se hizo clic derecho sobre una clase'
            self.box = box
            self.group = group
            self.popup.show(event, new=False)

    def remove_selected_box(self):
        self.classes.remove(self.box.model)
        self.group.remove()

