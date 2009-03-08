# -*- encoding: utf-8 -*-
import gtk
import gaphas
import gaphas.examples
import math

def distance((x1, y1), (x2, y2)):
    ca = x1 - x2
    co = y1 - y2
    return math.sqrt(ca*ca + co*co)


class Box(gaphas.examples.Item):

    def __init__(self, model, canvas_view):
        self.lines_connected_to_me = []
        self.canvas_view = canvas_view
        self.model = model
        gaphas.examples.Item.__init__(self)
        self.width = 100
        self.height = 100

    def a(self, widget):
        print widget

    def update_lines(self):
        "Actualiza la posición de las lineas que lo conectan a otras cajas."

        for line in self.lines_connected_to_me:
            line.update()


    def draw(self, context):
        name_font = 'sans bold 14'
        normal_font = 'sans 14'

        cr = context.cairo
        p = 10  # padding

        name = self.model.name
        atributes = "\n".join(self.model.variables)
        atributes_len_lines = len(self.model.variables)

        methods = "\n".join(self.model.methods)
        methods_len_lines = len(self.model.methods)

        # Estrategia para crear la caja
        # -----------------------------
        #
        # Medir el tamaño de todos los textos,
        # colocarlo en la lista sizes.
        #
        # (la lista tiene el formato [(ancho, alto), ...]
        # donde el primer elemento es el titulo, el segundo
        # los atributos y el tercero los métodos).

        gaphas.util.text_set_font(cr, name_font)
        name_size = gaphas.util.text_extents(cr, name) 

        gaphas.util.text_set_font(cr, normal_font)

        atributes_size = gaphas.util.text_extents(cr, atributes, multiline=True)
        # Inserta el calculo por separacion de lineas.
        w, h = atributes_size
        h += atributes_len_lines * 2
        atributes_size = (w, h)

        methods_size = gaphas.util.text_extents(cr, methods, multiline=True)
        # Inserta el calculo por separacion de lineas.
        w, h = methods_size
        h += methods_len_lines * 2
        methods_size = (w, h)

        sizes = [name_size, atributes_size, methods_size]

        # Obtiene el tamaño contenedor de la caja
        only_widths = [s[0] for s in sizes]
        max_width = max(only_widths)

        max_height = p * 2

        for w, h in sizes:
            max_height += h

        # Dibujar la caja con el tamaño caculado previamente.
        self._draw_box(context, cr, max_width, max_height, p)
        self._draw_lines(context, cr, sizes, max_width, p)

        # Positional counters (for draw)
        center_x = max_width / 2.0
        y = 0

        # Se imprimen todos los textos.
        gaphas.util.text_set_font(cr, name_font)
        gaphas.util.text_align(cr, center_x, y, name, 0, 1)

        x = center_x - sizes[1][0] / 2
        y = sizes[0][1] + p * 2
        gaphas.util.text_set_font(cr, normal_font)
        gaphas.util.text_multiline(cr, x, y, atributes)

        # Draw Methods
        y = sizes[1][1] + sizes[0][1] + p * 4
        x = center_x - sizes[2][0] / 2
        gaphas.util.text_multiline(cr, x, y, methods)

        #self.update_lines()

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

    def get_control_points(self):
        """Retorna los puntos situados en el borde de la caja.

        Estos puntos se utilizan para conectar lineas a otras cajas.
        """
        rect = self.canvas_view.get_item_bounding_box(self)

        x1, y1 = rect.x, rect.y
        x2, y2 = rect.x1, rect.y1
        w = rect.x1 - rect.x
        h = rect.y1 - rect.y

        return [(x1 + w/2, y1),
                (x1, y1 + h/2),
                (x2, y1 + h/2),
                (x1 + w/2, y2)]

    def _draw_box(self, context, cr, width, height, p):
        cr.save()
        # draw background
        if context.focused:
            cr.set_source_rgb(0.9, 0.9, 1)
        elif context.hovered:
            cr.set_source_rgb(0.9, 1, 0.9)
        else:
            cr.set_source_rgb(1, 1, 1)

        cr.rectangle(0 - p, 0 -p, width + p * 2, height + p * 4)
        cr.fill()


        # draw border
        if context.selected:
            cr.set_source_rgb(0, 0, 1)
        else:
            cr.set_source_rgb(0, 0, 0)

        cr.rectangle(0 - p, 0 -p, width + p * 2, height + p * 4)
        cr.stroke()

        cr.restore()

    def _draw_lines(self, context, cr, sizes, width, p):
        y = sizes[0][1] + p

        # draw border
        if context.selected:
            cr.set_source_rgb(0, 0, 1)
        else:
            cr.set_source_rgb(0, 0, 0)

        # Line between 'name' and 'attributes'
        self._draw_horizontal_line(cr, -p, sizes[0][1] + p, width + p)

        # Line between 'attributes' and 'methods'
        self._draw_horizontal_line(cr, -p, sizes[0][1] + sizes[1][1] + p * 3, width + p)

        cr.set_source_rgb(0, 0, 0)

    def _draw_horizontal_line(self, cr, x, y, width):
        cr.save()
        cr.move_to(x, y)
        cr.line_to(width, y)
        cr.stroke()
        cr.restore()

    def inspect(self):
        print self
        self.model.inspect()

        if self.lines_connected_to_me:
            for i, line in enumerate(self.lines_connected_to_me):
                print "\tlines_connected_to_me[%d]: %s" %(i, line)
        else:
            print "\tno lines connected to me"

    # Manejo de lineas
    def get_outgoing_lines(self):
        father_list = [line for line in self.lines_connected_to_me
            if line.child == self]
        return father_list
    
    def get_incoming_lines(self):
        child_list = [line for line in self.lines_connected_to_me
            if line.father == self]

        return child_list
