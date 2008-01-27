import goocanvas
import pango


class Box:

    def __init__(self, x, y, model, root):
        self.model = model
        self._create_view(root)
        self.group.translate(x, y)
        self.update(model)

    def _create_view(self, root):
        self.group = goocanvas.Group()
        root.add_child(self.group)

        self.box = goocanvas.Rect(stroke_color='black',
                line_width=2.0, fill_color='white', radius_x=5, radius_y=5)
        self.title = goocanvas.Text(text='Hola', font='Arial 10',
                fill_color='black', use_markup=True, 
                alignment=pango.ALIGN_CENTER)
        self.attributes = goocanvas.Text(font='Arial 10', text='', 
                fill_color='black', alignment=pango.ALIGN_CENTER)
        self.methods = goocanvas.Text(font='Arial 10', text='', 
                fill_color='black', alignment=pango.ALIGN_CENTER)
        self.line1 = goocanvas.Path(data="",
                stroke_color="black", line_width=2.0)
        self.line2 = goocanvas.Path(data="",
                stroke_color="black", line_width=2.0)

        self.group.add_child(self.box)
        self.group.add_child(self.title)
        self.group.add_child(self.attributes)
        self.group.add_child(self.methods)
        self.group.add_child(self.line1)
        self.group.add_child(self.line2)

    def concatenate(self, a, b):
        return "%s\n%s" %(a, b)

    def update(self, model):

        if model.abstract:
            self.title.props.text = "<i><b>%s</b></i>" % model.name
        else:
            self.title.props.text = "<b>%s</b>" % model.name

        if model.variables:
            self.attributes.props.text = reduce(self.concatenate, model.variables)
        if model.methods:
            self.methods.props.text = reduce(self.concatenate, model.methods)

        self.update_positions()

    def dy(self, object):
        bounds = object.get_bounds()
        return bounds.y2 - bounds.y1

    def dx(self, object):
        bounds = object.get_bounds()
        return bounds.x2 - bounds.x1

    def update_positions(self):
        dx1 = self.dx(self.title)
        dy1 = self.dy(self.title)
        self.attributes.translate(0, dy1 + 10)

        dy2 = self.dy(self.attributes)
        dx2 = self.dx(self.attributes)
        self.methods.translate(0, dy1 + dy2 + 10 + 10)

        dx3 = self.dx(self.methods)
        dy3 = self.dy(self.methods)

        width = max(dx1, dx2, dx3) + 10
        
        self.box.props.x -= 5
        self.box.props.y -= 5
        self.box.props.width = width
        self.box.props.height = dy1 + dy2 + dy3 + 30

        self.line1.props.data = "M -5 %d L %d %d" %(dy1 + 5, width -5, dy1 + 5)
        self.line2.props.data = "M -5 %d L %d %d" %(dy1 + dy2 + 15, width -5, 
                dy1 + dy2 + 15)
