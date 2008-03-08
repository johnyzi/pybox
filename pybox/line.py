# -*- coding: utf-8 -*-
import gtk
import goocanvas
import math
import pydb



class Box1(goocanvas.Rect):

    def __init__(self, x, y):
        goocanvas.Rect.__init__(self, x=x, y=y, width=50, height=50, 
                line_width=2.0, stroke_color="black", fill_color="#eee")

    def get_connection_more_closer_to(self, other):
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

    def get_control_points(self):
        bounds = self.get_bounds()
        x1, y1 = bounds.x1, bounds.y1
        x2, y2 = bounds.x2, bounds.y2
        w, h = x2 - x1, y2 - y1

        #    (x1, y1)    (x1 + w/2, y1)    (x2, y1)
        #
        #        +-------------+--------------+
        #        |                            |
        #        |                            |
        #        + (x1, y1 + h/2)             + (x2, y1 + h/2)
        #        |                            |
        #        |                            |
        #        +-------------+--------------+
        #
        #    (x1, y2)    (x1 + w/2, y2)    (x2, y2)


        return [
                #(x1, y1),
                (x1 + w/2, y1),
                #(x2, y1),
                (x1, y1 + h/2),
                (x2, y1 + h/2),
                #(x1, y2),
                (x1 + w/2, y2),
                #(x2, y2)
                ]

class Line(goocanvas.Polyline):
    "Representa una linea que conecta a dos modelos de clase."

    def __init__(self, child_box, parent_box, root):
        self.child = child_box
        self.father = parent_box
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
        #self.child.lines_connected_to_me.remove(self)
        #self.father.lines_connected_to_me.remove(self)
        goocanvas.Polyline.remove(self)
        print "remove, ",self




'''
lines = None
dragging = False
drag_x = 0
drag_y = 0


def on_button_press_event(item, target, event):
    global dragging, drag_x, drag_y

    if event.button == 1:
        drag_x = event.x
        drag_y = event.y
        dragging = True
    
def on_button_release_event(item, target, event):
    global dragging
    dragging = False

def on_motion_notify_event(item, target, event):
    global dragging, drag_x, drag_y

    if dragging:
        new_x = event.x
        new_y = event.y
        item.translate(new_x - drag_x, new_y - drag_y)
        bounds = item.get_bounds()
        x, y = bounds.x1, bounds.y1

        for f in lines:
            f.update()


# creación de la ventana
window = gtk.Window()
window.connect("destroy", gtk.main_quit)
window.set_position(gtk.WIN_POS_CENTER)

# creación del Canvas
canvas = goocanvas.Canvas()
window.add(canvas)

# construcción del rectángulo
box1 = Box(20, 20)
box2 = Box(100, 100)
box3 = Box(170, 80)

# eventos asociados al desplazamiento de objetos
box1.connect("button_press_event", on_button_press_event)
box1.connect("button_release_event", on_button_release_event)
box1.connect("motion_notify_event", on_motion_notify_event)

box2.connect("button_press_event", on_button_press_event)
box2.connect("button_release_event", on_button_release_event)
box2.connect("motion_notify_event", on_motion_notify_event)

box3.connect("button_press_event", on_button_press_event)
box3.connect("button_release_event", on_button_release_event)
box3.connect("motion_notify_event", on_motion_notify_event)


# se agregan al nodo principal
root = canvas.get_root_item()
root.add_child(box1)
root.add_child(box2)
root.add_child(box3)

linea1 = Line(box2, box1)
linea2 = Line(box3, box1)

root.add_child(linea1)
root.add_child(linea2)

lines = [linea1, linea2]

lines = [linea1, linea2]

# bucle principal
window.show_all()
gtk.main()
'''
