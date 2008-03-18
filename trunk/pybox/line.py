# -*- coding: utf-8 -*-
import gtk
import goocanvas


class Line(goocanvas.Polyline):
    "Representa una linea que conecta a dos modelos de clase."

    def __init__(self, child_box, father_box, root):
        self.child = child_box
        self.father = father_box
        goocanvas.Polyline.__init__(self, end_arrow=True)
        self.update()
        root.add_child(self)
        self.child.lines_connected_to_me.append(self)
        self.father.lines_connected_to_me.append(self)

    def update(self):
        "Actualiza los puntos que conectan a la linea con dos clases."
        closers = self.child.get_connection_more_closer_to(self.father)
        self.props.points = goocanvas.Points(closers)

    def remove(self):

        self.child.lines_connected_to_me.remove(self)
        self.father.lines_connected_to_me.remove(self)

        goocanvas.Polyline.remove(self)

    def __repr__(self):
        src = self.child.model.name
        dst = self.father.model.name
        return "<Line instance from '%s' to '%s'>" %(src, dst)
