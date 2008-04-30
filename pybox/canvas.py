# -*- encoding: utf-8 -*-
import gtk
import goocanvas

import line
import popup
import session
from box import Box
import dialogs
import config
import pango

class Canvas(goocanvas.Canvas):

    # Stores the position where right click was pressed.
    x_position = 0
    y_position = 0

    def __init__(self, main):
        goocanvas.Canvas.__init__(self)
        self.main = main
        self.boxes = []
        self.connect('event', self.on_event)
        #self.connect('button_press_event', self.on_button_press)
        self._create_session()
        self.popup = popup.Popup(self)

        #self._create_help_text()
        self.show()
        self.new()

    '''
    def _create_help_text(self):
        text = "use double click to create a class."
        props = {
                'font': config.SMALL_FONT,
                'text': text,
                'alignment': pango.ALIGN_LEFT,
                'fill_color': '#777',
                'use_markup': True,
                'x': 20,
                'y': 20,
                }
        root = self.get_root_item()
        self._help_text = goocanvas.Text(** props)
        root.add_child(self._help_text)
    '''

    def _create_session(self):
        self.session = session.Session(self.main)

    def new(self):
        """Returns: True if creates a new document."""
        if self.show_confirm_save_dialog():
            self.session.new_document_notify()
            self._clear()
            return True

    def show_confirm_save_dialog(self):
        """Muestra un cuadro de dialogo consultando si desea guardar los cambios.

        Si el usuario logra guardar al momento de mostrarse el cuadro o bien
        acepta perder cualquier cambio se devuelve True, en caso contrario si el
        usuario cancela la operación o no logra guardar devuelve False."""

        if self.session.can_leave(self.save):
            return True

    def open(self, filename):
        self.session.open_document_notify(filename)
        self._clear()

    def _clear(self):
        self._create_new_canvas_area()
        #self._set_help_text_visible(True)

        for box in self.boxes:
            box.remove()

        self.boxes = []

    def _create_new_canvas_area(self):
        self.props.x1 = 0
        self.props.y1 = 0
        self.props.x2 = 300
        self.props.y2 = 170

    def on_event(self, widget, event):
        "Show a menu when right click is pressed over the canvas."

        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            self.popup.show(event, new=True)
            self.x_position = event.x
            self.y_position = event.y
            return True
        '''
        elif event.type == gtk.gdk._2BUTTON_PRESS:
            # TODO: Modularizar la creacion en otra clase
            self.x_position = event.x
            self.y_position = event.y
            self.popup.on_add__activate(None)
        '''

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

        self.session.on_notify_create_class(new_model)
        #self._set_help_text_visible(False)

    '''
    def _set_help_text_visible(self, state):
        pass
    '''

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
                child.model.superclass.append(father.model.name)


    def _search_relation(self, box, superclass, old_fathers):
        
        #Busca si se genera un bucle para romperlo
        fathers = box.get_outgoing_lines()
        for line in fathers:
            if line.father == superclass:
                line.child.model.superclass.remove(superclass.model.name)
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

        old_fathers = [line.father for line in self.box.get_outgoing_lines()]
        for line in self.box.get_incoming_lines():
            line.child.model.superclass.remove(self.box.model.name)
            self._reconnect_herency(line.child, old_fathers)
            line.remove()

        self.box.remove()
        self.session.on_notify_remove_class(self.box.model)

    def update_area_expanding(self, bounds):
        "Expand canvas area (if necessary) to content this box."

        redraw = False

        if bounds.x1 < 0:     # left border
            self.props.x2 = self.props.x2 + abs(bounds.x1)
            redraw = True
        
        elif bounds.x2 > self.props.x2:   # right border
            self.props.x2 = bounds.x2

        if bounds.y1 < 0:     # upper border
            self.props.y2 = self.props.y2 + abs(bounds.y1)
            redraw = True
        
        elif bounds.y2 > self.props.y2:   # bottom border
            self.props.y2 = bounds.y2

        return redraw


    # TODO: cambiar el nombre de método, dado que el siguiente método se llama
    # al terminar de arrastrar una caja, y su nombre actual es una
    # consecuencia de esa acción y no es muy general.
    def update_area_to_contract(self):
        "Contract the canvas area to save space."

        #TODO: Buscar otra forma de reducir el area de pantalla, el siguiente
        #      código funciona correctamente pero hace poco manipulable el
        #      area de pantalla.

        #self.session.on_notify_move_class(self.model)

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

    def __repr__(self):
        return "<Canvas instance>"

    def inspect(self):
        print self

        for i, line in enumerate(self.boxes):
            print "\tboxes[%d]: %s" %(i, line)

        for box in self.boxes:
            print ""
            box.inspect()

    def save(self, extra=None):
        main = self.main.view.main
        status = self.main.view.status
        dialog = dialogs.save.Document(main, self, status)
        return dialog.run()

    def open_dialog(self):
        dialogs.open.Document(self.main.view.main, self, self.main.view.status)

    def save_as(self, extra=None):
        self.save()

if __name__ == '__main__':
    canvas = Canvas(main=None)
    canvas.inspect()
