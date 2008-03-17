# -*- encoding: utf-8 -*-
import goocanvas
from box import Box
import line
import gtk
import popup

class Canvas(goocanvas.Canvas):

    # Stores the position where right click was pressed.
    x_position = 0
    y_position = 0

    def __init__(self, main):
        goocanvas.Canvas.__init__(self)
        self.main = main
        self.boxes = []
        self.props.x2 = 100
        self.props.y2 = 100
        self.show()
        self.connect('event', self.on_event)

        self.popup = popup.Popup(self)

    def clear(self):
        self.props.x1 = 0
        self.props.y1 = 0
        self.props.x2 = 100
        self.props.y2 = 100

        for box in self.boxes:
            box.remove()

        self.boxes = []

    def on_event(self, widget, event):
        "Show a menu when right click is pressed over the canvas."

        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            self.popup.show(event, new=True)
            self.x_position = event.x
            self.y_position = event.y

    def create_box(self, new_model, x=None, y=None, hierarchy_lines=True):
        """Create a graphical Box that shows a class model.

            `x`: horizontal position.
            `y`: vertical position.
            `hierarchy_lines`: if must do connect hierarchy lines.
        """
        root = self.get_root_item()

        # Si no se especifican `x` e `y` como parametros se asume
        # que ha creado la caja desde el menú desplegable `Popup`.
        if not x and not y:
            x = self.x_position + self.props.x1
            y = self.y_position + self.props.y1

        box = Box(x, y, new_model, root, self)
        box.group.connect('button_press_event', self.on_button_press_event, box)
        self.boxes.append(box)

        if hierarchy_lines:
            self.connect_box(box, new_model)

        self.main.view.status.info("Creating %s class" %(new_model.name))

    def connect_box(self, box, new_model):

        # Conecta a las cajas en caso de existir una relacion.
        father_lines = box.get_outgoing_lines()
        old_fathers = []
        for line in father_lines:
            old_fathers.append(line.father)
            line.remove()
        
        if new_model.superclass:
            for father in new_model.superclass:
                superclass_box = self.get_box_by_name(father)
                self.create_line(box, superclass_box)
                superclass = self.get_box_by_name(new_model.name)
                self._search_relation(superclass_box, superclass, old_fathers)

    def _reconnect_herency(self, child, old_fathers):

        #Reconecta un hijo de un box con los antiguos padres de este ultimo.
            for father in old_fathers:
                self.create_line(child, father)
                child.model.superclass.append(father)


    def _search_relation(self, box, superclass, old_fathers):
        
        #Busca si se genera un bucle para romperlo
        fathers = box.get_outgoing_lines()
        for line in fathers:
            if line.father == superclass:
                self._reconnect_herency(line.child, old_fathers)
                line.remove()
            self._search_relation(line.father, superclass, old_fathers)

    def get_model_by_name(self, name):
        box = self.get_box_by_name(name)
        return box.model

    def get_class_names(self):
        return [box.model.name for box in self.boxes]

    def get_box_by_name(self, name):
        for box in self.boxes:
            if box.model.name == name:
                return box
        else:
            raise NameError("This class box don't exist", name)

    def create_line(self, child_model, parent_model):
        root = self.get_root_item()
        line.Line(child_model, parent_model, root)

    def on_button_press_event(self, group, widget, event, box):
        # Almacenamos el box y el grupo para que pueda ser accedido por el
        # evento on_remove__activate o on_edit__activate.
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            self.box = box
            self.group = group
            self.popup.show(event, new=False)

    def remove_selected_box(self):
        name = self.box.model.name
        self.boxes.remove(self.box)

        old_fathers = [line.fahter for line in self.box.get_outgoing_lines()]
        for line in self.box.get_incoming_lines():
            self._reconnect_herency(line.child, old_fathers)

        self.box.remove()
        self.main.view.status.info("Removing %s class" %(name))

    def update_area_expanding(self, bounds):
        "Expand canvas area (if necessary) to content this box."

        if bounds.x1 < self.props.x1:     # left border
            self.props.x1 = bounds.x1
        elif bounds.x2 > self.props.x2:   # right border
            self.props.x2 = bounds.x2

        if bounds.y1 < self.props.y1:     # upper border
            self.props.y1 = bounds.y1
        elif bounds.y2 > self.props.y2:   # bottom border
            self.props.y2 = bounds.y2


    def update_area_to_contract(self):
        "Contract the canvas area to save space."

        #TODO: Buscar otra forma de reducir el area de pantalla, el siguiente
        #      código funciona correctamente pero hace poco manipulable el
        #      area de pantalla.

        '''
        box_list = [box for box in self.boxes]

        minus_left = box_list[0].get_left()

        for box in box_list:
            left = box.get_left()

            if left < minus_left:
                left = minus_left

        if self.props.x1 < minus_left:
            self.props.x1 = minus_left
        '''
