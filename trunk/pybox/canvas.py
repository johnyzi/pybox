# -*- encoding: utf-8 -*-
import goocanvas
import box
import line
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
        self.boxes = []

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

    def create_box(self, new_model, x=None, y=None):
        root = self.get_root_item()

        # Si no se especifican `x` e `y` como parametros se asume
        # que ha creado la caja desde el menú desplegable `Popup`.
        if not x and not y:
            x = self.x_position
            y = self.y_position

        box1 = box.Box(x, y, new_model, root)
        box1.group.connect('button_press_event', self.on_button_press_event, box1)
        self.classes.append(new_model)
        self.boxes.append((new_model.name, box1))

        self.connect_box(box1, new_model)

    def connect_box(self, box, new_model):
        # Conecta a las cajas en caso de existir una relacion.
        if new_model.superclass:
            superclass_box = self.get_box_by_name(new_model.superclass)
            self.create_line(box, superclass_box)

    def get_model_by_name(self, name):
        for model in self.classes:
            if model.name == name:
                return model
        else:
            raise NameError("No existe la clase de nombre", name)

    def get_box_by_name(self, name):
        for boxname, box in self.boxes:
            if boxname == name:
                return box
        else:
            raise NameError("No existe la clase de nombre", name)

    def create_line(self, child_model, parent_model):
        root = self.get_root_item()
        line.Line(child_model, parent_model, root)

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
        self.box.remove()

