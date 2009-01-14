# -*- encoding: utf-8 -*-
import gtk
import gaphas
import gaphas.examples

def distance((x1, y1), (x2, y2)):
    ca = x1 - x2
    co = y1 - y2
    return math.sqrt(ca*ca + co*co)


class Box(gaphas.examples.Item):

    def __init__(self, model, canvas_view):
        self.model = model
        gaphas.examples.Item.__init__(self)
        self.width = 100
        self.height = 100

    def draw(self, context):
        cr = context.cairo
        cr.set_source_rgb(0, 0, 0)

        gaphas.util.text_set_font(cr, 'sans bold 14')

        text = self.model.name
        width, height = gaphas.util.text_extents(cr, text)
        p = 10  # padding

        # draw background
        if context.focused:
            cr.set_source_rgb(0.9, 0.9, 1)
        elif context.hovered:
            cr.set_source_rgb(0.9, 1, 0.9)
        else:
            cr.set_source_rgb(1, 1, 1)

        cr.rectangle(0 - p, 0 -p, width + p * 2, height + p * 2)
        cr.fill()

        # draw text
        cr.set_source_rgb(0, 0, 0)
        gaphas.util.text_align(cr, 0, 0, text, 1, 1)

        # draw border
        if context.selected:
            cr.set_source_rgb(0, 0, 1)
        else:
            cr.set_source_rgb(0, 0, 0)

        cr.rectangle(0 - p, 0 -p, width + p * 2, height + p * 2)
        cr.stroke()

