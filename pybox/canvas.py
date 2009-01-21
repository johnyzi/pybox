# -*- encoding: utf-8 -*-
import gtk
import gobject
import gaphas
from gaphas import tool

import popup
import session

import box
import model
import dialogs
import line

class Canvas(gaphas.view.GtkView):
    """Representa el objeto GTK que muestra el diagrama de clases."""

    def __init__(self, main):
        gaphas.view.GtkView.__init__(self)
        self.main = main
        self.boxes = []
        self.internal_zoom_factor = 1

        # Creates some internal objects
        self.session = session.Session(self.main)
        self.popup = popup.Popup(self)

        # Creates canvas drawable
        self.canvas = gaphas.canvas.Canvas()

        # Set only the used tools.
        new_tools = tool.ToolChain()
        new_tools.append(tool.HoverTool())
        new_tools.append(tool.HandleTool())
        new_tools.append(tool.ItemTool())
        new_tools.append(tool.RubberbandTool())

        self.tool = new_tools

        self.show()

        # Event handlers
        self.connect('event', self.on_event)

    def on_event(self, widget, event):
        """This method is called by gtk when user iteract with canvas.
        
        Now, only show a menu when right click is pressed over the canvas."""

        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            self.popup.show(event, True)
            self.x_position = event.x
            self.y_position = event.y


    def get_class_names(self):
        """Get a list with all class names."""
        return [box.model.name for box in self.boxes]

    def get_box_by_name(self, name):
        """Get a box instante by using a name."""

        for box in self.boxes:
            if box.model.name == name:
                return box
        else:
            raise NameError("This class box don't exist", name)

    def inspect(self):
        """Show some internal atributtes for this object."""
        print self

        for i, line in enumerate(self.boxes):
            print "\tboxes[%d]: %s" %(i, line)

        for box in self.boxes:
            print ""
            box.inspect()

    def show_create_class_dialog(self):
        new_model = model.Model()
        all_classes = self.get_class_names()

        dialog = dialogs.classview.ClassView(new_model, all_classes)
        response = dialog.view.dialog1.run()

        if response:
            self.create_box(new_model, 40, 40)

    def create_box(self, new_model, x=None, y=None, hierarchy_lines=True):
        """Create a graphical Box that shows a class model.

            `x`: horizontal position.
            `y`: vertical position.
            `hierarchy_lines`: if must do connect hierarchy lines.
        """
        new_box = box.Box(new_model, self)
        self.boxes.append(new_box)

        if x is None and y is None:
            x = self.x_position
            y = self.y_position

        new_box.matrix.translate(x, y)
        self.canvas.add(new_box)

        if hierarchy_lines:
            self.connect_box(new_box, new_model)

    def connect_box(self, box, model):
        # Conecta a las cajas en caso de existir una relacion.
        father_lines = box.get_outgoing_lines()
        old_fathers = []

        for line in father_lines:
            old_fathers.append(line.father)
            line.remove()

        if model.superclass:
            for father in model.superclass:
                superclass_box = self.get_box_by_name(father)
                self.create_line(box, superclass_box)
                superclass = self.get_box_by_name(model.name)

    def create_line(self, child, father):
        new_line = line.Line(self, child, father)
        self.canvas.add(new_line)

    def focus(self):
        self.main.view.status.ui.get_widget('debug').grab_focus()
        self.main.canvas.grab_focus()
        self.main.canvas.emit("button-press-event", gtk.gdk.Event(gtk.gdk.NOTHING))
        self.main.canvas.emit("button-release-event", gtk.gdk.Event(gtk.gdk.NOTHING))


    # Cambio de escala
    def zoom_in(self):
        self.zoom(1.2)
        self.internal_zoom_factor += 1.2

    def zoom_out(self):
        self.zoom(1/1.2)
        self.internal_zoom_factor -= 1.2
