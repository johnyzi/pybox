# -*- coding: utf-8 -*-
import gtk
import gaphas


class Line(gaphas.examples.Item):

    def __init__(self, canvas_view, child, father):
        gaphas.examples.Item.__init__(self)
        self.set_points((10, 10), (30, 30))

        self.child = child
        self.father = father

        self.child.lines_connected_to_me.append(self)
        self.father.lines_connected_to_me.append(self)

    def set_points(self, start, end):
        self.start = start
        self.end = end

    def draw(self, context):
        cr = context.cairo

        cr.save()
        cr.move_to(*self.start)
        cr.line_to(*self.end)
        cr.stroke()
        cr.restore()

        x, y = self.end

        '''
        # Punta de la flecha
        cr.save()
        cr.move_to(x, y)
        cr.line_to(x, y - 5)
        cr.line_to(x + 10, y)
        cr.line_to(x, y + 5)
        cr.close_path()
        cr.fill()
        cr.restore()
        '''

    def update(self):
        closers = self.child.get_connection_more_closer_to(self.father)
        self.set_points(closers[0], closers[1])
        self.request_update()

class Ldine(gaphas.item.Line):

    def __init__(self, canvas_view, child, father):
        gaphas.item.Line.__init__(self)
        self.canvas_view = canvas_view

        self.child = child
        self.father = father

        self.child.lines_connected_to_me.append(self)
        self.father.lines_connected_to_me.append(self)

    def set_points(self, p1, p2):
        self.handles()[0].pos = p1
        self.handles()[1].pos = p2

    def update(self):
        "Actualiza los puntos que conectan a la linea con dos clases."

        #print self.canvas_view.get_item_bounding_box(self.father)

        closers = self.child.get_connection_more_closer_to(self.father)
        self.set_points(closers[0], closers[1])
        self.request_update()

    def draw_taisl(self, context):
        cr = context.cairo
        # la linea
        cr.line_to(0, 0)
        cr.stroke()

        # la punta de flecha
        cr.save()
        cr.line_to(10, 5)
        cr.move_to(0, 0)
        cr.line_to(10, -5)
        cr.line_to(10, 5)
        cr.close_path()
        cr.fill()
        cr.restore()

    def remove(self):
        self.child.lines_connected_to_me.remove(self)
        self.father.lines_connected_to_me.remove(self)

    def __repr__(self):
        src = self.child.model.name
        dst = self.father.model.name
        return "<Line instance from '%s' to '%s'>" %(src, dst)
'''
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
'''
