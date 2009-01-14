# -*- encoding: utf-8 -*-
import gtk
import gobject
import gaphas

import popup
import session

class Canvas(gaphas.view.GtkView):

    def __init__(self, main):
        gaphas.view.GtkView.__init__(self)
        self.main = main
        self.boxes = []

        # Creates some internal objects
        self.session = session.Session(self.main)
        self.popup = popup.Popup(self)

        # Creates canvas drawable
        self.canvas = gaphas.canvas.Canvas()
        self.show()

        # Event handlers
        self.connect('event', self.on_event)


    def on_event(self, widget, event):
        """This method is called by gtk when user iteract with canvas.
        
        Now, only show a menu when right click is pressed over the canvas."""

        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            self.popup.show(event, new=True)
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


    def create_box(self, new_model, x=None, y=None, hierarchy_lines=True):
        """Create a graphical Box that shows a class model.

            `x`: horizontal position.
            `y`: vertical position.
            `hierarchy_lines`: if must do connect hierarchy lines.
        """
        box = box.Box(x, y, new_model, self)
        self.boxes.append(box)
