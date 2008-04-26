# -*- encoding: utf-8 -*-
import gtk
import goocanvas
import math
import config
import common

def distance((x1, y1), (x2, y2)):
    ca = x1 - x2
    co = y1 - y2
    return math.sqrt(ca*ca + co*co)

class Box:
    """
    Representa una caja que visualiza el modelo de datos.

    La caja conoce el modelo de datos que representa y a su vez a todas
    las lineas que lo conectan con otras cajas (padres o hijos de ella).
    """

    def __init__(self, x, y, model, root, canvas):
        self.lines_connected_to_me = []
        self.model = model
        self.canvas = canvas
        self._create_view(root)
        self.x = x
        self.y = y
        self.group.translate(x + 5, y + 5)
        self.update(model)
        self._init_drag_feature()

    def _init_drag_feature(self):
        self.dragging = False
        self.drag_x = 0
        self.drag_y = 0
        self.group.connect('button_press_event', self.on_button_press)
        self.group.connect('button_release_event', self.on_drag_end)
        self.group.connect('motion_notify_event', self.on_motion)

    def remove(self):
        for line in self.lines_connected_to_me:
            line.remove()

        self.group.remove()

    def on_button_press(self, group, item, event):
        group.raise_(None)

        if event.button == 1:
            if event.type == gtk.gdk._2BUTTON_PRESS:
                self.canvas.popup.on_edit__activate(None, box=self)
                self.dragging = False
            else:
                # Arrastrar y soltar
                self.dragging = True
                self.drag_x = event.x
                self.drag_y = event.y

    def on_drag_end(self, group, item, event):
        self.dragging = False
        self.canvas.session.on_notify_move_class(self.model)
        self.canvas.update_area_to_contract()

    def on_motion(self, group, item, event):

        if self.dragging:

            dx = event.x - self.drag_x
            dy = event.y - self.drag_y
            group.translate(dx, dy)
            self.update_lines()
            redraw = self.canvas.update_area_expanding(self.group.get_bounds())

            if redraw:
                self._redraw_boxes(-1*dx, -1*dy)

            bounds = group.get_bounds()
            self.x = bounds.x1 - 5
            self.y = bounds.y1 - 5

    def _redraw_boxes(self, dx, dy):

        #Redibuja boxes para simular un corrimiento hacia arriba o izquierda
        for box in self.canvas.boxes:
            box.group.translate(dx, dy)
            box.update_lines()
            box.canvas.update_area_expanding(box.group.get_bounds())



    def update_lines(self):
        "Actualiza la posición de las lineas que lo conectan a otras cajas."

        for line in self.lines_connected_to_me:
            line.update()

    def _create_view(self, root):
        self.group = goocanvas.Group()
        root.add_child(self.group)

        text_theme = common.config.text_theme
        box_theme = common.config.box_theme
        division_theme = common.config.division_theme

        self.box = goocanvas.Rect(**box_theme)
        self.title = goocanvas.Text(**text_theme)
        self.attributes = goocanvas.Text(**text_theme)
        self.methods = goocanvas.Text(**text_theme)
        self.line1 = goocanvas.Path(**division_theme)
        self.line2 = goocanvas.Path(**division_theme)

        self.group.add_child(self.box)
        self.group.add_child(self.title)
        self.group.add_child(self.attributes)
        self.group.add_child(self.methods)
        self.group.add_child(self.line1)
        self.group.add_child(self.line2)

    def concatenate(self, a, b):
        return "%s\n%s" %(a, b)

    def update(self, model, last_name=None):

        if model.abstract:
            self.title.props.text = "<i><b>%s</b></i>" % model.name
        else:
            self.title.props.text = "<b>%s</b>" % model.name

        if model.variables:
            self.attributes.props.text = reduce(self.concatenate, model.variables)
        else:
            self.attributes.props.text = ""

        if model.methods:
            self.methods.props.text = reduce(self.concatenate, model.methods)
        else:
            self.methods.props.text = ""

        self.update_positions()
        self.canvas.update_area_expanding(self.group.get_bounds())
        self._update_childs(last_name)

    def _update_childs(self, last_name):
        for line in self.get_incoming_lines():
            print "Antes se llamaba", last_name
            print "   y ahora se llama", self.model.name
            line.child.model.superclass.remove(last_name)
            line.child.model.superclass.append(self.model.name)

    def dy(self, object):
        bounds = object.get_bounds()
        return bounds.y2 - bounds.y1

    def dx(self, object):
        bounds = object.get_bounds()
        return bounds.x2 - bounds.x1

    def get_control_points(self):
        """Retorna los puntos situados en el borde de la caja.

        Estos puntos se utilizan para conectar lineas a otras cajas.
        """
        bounds = self.group.get_bounds()
        x1, y1 = bounds.x1, bounds.y1
        x2, y2 = bounds.x2, bounds.y2
        w, h = x2 - x1, y2 - y1

        return [(x1 + w/2, y1),
                (x1, y1 + h/2),
                (x2, y1 + h/2),
                (x1 + w/2, y2)]

    def get_connection_more_closer_to(self, other):
        "Retorna los puntos mas cercanos para conectar dos cajas."
        my_control_points = self.get_control_points()
        he_control_points = other.get_control_points()
        less_distance = 400
        points = []

        for my_point in my_control_points:
            for he_point in he_control_points:
                dist = distance(my_point, he_point)

                if not points:
                    points = [my_point, he_point]
                    less_distance = dist
                elif dist < less_distance:
                    points = [my_point, he_point]
                    less_distance = dist

        return points

    def update_positions(self):
        dx1 = self.dx(self.title)
        dy1 = self.dy(self.title)
        self.attributes.props.y = dy1 + 10

        dy2 = self.dy(self.attributes)
        dx2 = self.dx(self.attributes)
        self.methods.props.y = dy1 + dy2 + 10 + 10

        dx3 = self.dx(self.methods)
        dy3 = self.dy(self.methods)
        
        width = max(dx1, dx2, dx3) + 10
        "Centra el texto de las cajas de atributo titulo y de metodos"
        width_text = max(dx1, dx2, dx3)
        self.title.props.width = width_text
        self.attributes.props.width = width_text
        self.methods.props.width = width_text
        "Fin del centrado"
        self.box.props.x = -5
        self.box.props.y = -5
        self.box.props.width = width
        self.box.props.height = dy1 + dy2 + dy3 + 30

        self.line1.props.data = "M -5 %d L %d %d" %(dy1 + 5, width -5, dy1 + 5)
        self.line2.props.data = "M -5 %d L %d %d" %(dy1 + dy2 + 15, width -5, 
                dy1 + dy2 + 15)

    def get_left(self):
        bound = self.group.get_bounds()
        return bound.x1

    def get_outgoing_lines(self):

        father_list = [line for line in self.lines_connected_to_me
            if line.child == self]
        return father_list
    
    def get_incoming_lines(self):
        child_list = [line for line in self.lines_connected_to_me
            if line.father == self]

        return child_list

    def __repr__(self):
        return "<Box instance of '%s' class>" %(self.model.name)

    def inspect(self):
        print self
        self.model.inspect()

        for i, line in enumerate(self.lines_connected_to_me):
            print "\tlines_connected_to_me[%d]: %s" %(i, line)
