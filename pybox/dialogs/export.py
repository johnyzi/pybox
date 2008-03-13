# -*- encoding: utf-8 -*-
import cPickle
import gtk
import cairo
import goocanvas

class SaveDialog:

    def __init__(self, parent, canvas, status, pattern, name):
        self.canvas = canvas
        self.parent = parent
        self.status = status
        self._create_dialog(pattern, name)
        self._run()

    def _create_dialog(self, pattern, name):
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                gtk.STOCK_SAVE, gtk.RESPONSE_OK)
        action = gtk.FILE_CHOOSER_ACTION_SAVE 

        dialog = gtk.FileChooserDialog(action=action, 
                buttons=buttons,
                parent=self.parent)
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_name(name)


        # Filtro personalizado
        filter = gtk.FileFilter()
        label, mask = pattern
        filter.set_name(label)
        filter.add_pattern(mask)
        dialog.add_filter(filter)

        # Filtro (*)
        filter = gtk.FileFilter()
        filter.set_name("All Files")
        filter.add_pattern("*")
        dialog.add_filter(filter)
        self.dialog = dialog

    def _run(self):
        response = self.dialog.run()

        if response == gtk.RESPONSE_OK:
            self._save_canvas_to(self.dialog.get_filename())

        self.dialog.hide()


class PNG(SaveDialog):
    """Allow to export canvas area in a .PNG file."""

    def __init__(self, parent, canvas, status):
        pattern = ("PNG Files", "*.png")
        name = "untitled.png"
        SaveDialog.__init__(self, parent, canvas, status, pattern, name)

    def _save_canvas_to(self, filename):
        width = self.canvas.props.x2 - self.canvas.props.x1
        height = self.canvas.props.y2 - self.canvas.props.y1

        bounds = goocanvas.Bounds(* self.canvas.get_bounds())

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))
        cr = cairo.Context(surface)
        self.canvas.render(cr, bounds, 1.0)
        cr.show_page()

        try:
            surface.write_to_png(filename)
        except IOError:
            self.status.error("I can't write the file as %s." %filename)
            return

        self.status.info("File saved as %s" %filename)


class PDF(SaveDialog):
    """Allow to export canvas area in a .PDF file."""

    def __init__(self, parent, canvas, status):
        pattern = ("PDF Files", "*.pdf")
        name = "untitled.pdf"
        SaveDialog.__init__(self, parent, canvas, status, pattern, name)

    def _save_canvas_to(self, filename):
        width = self.canvas.props.x2 - self.canvas.props.x1
        height = self.canvas.props.y2 - self.canvas.props.y1

        bounds = goocanvas.Bounds(* self.canvas.get_bounds())

        try:
            surface = cairo.PDFSurface(filename, int(width), int(height))
        except IOError:
            self.status.error("I can't write the file as %s." %filename)
            return

        cr = cairo.Context(surface)
        self.canvas.render(cr, bounds, 1.0)
        cr.show_page()
        self.status.info("File saved as %s" %filename)

class Document(SaveDialog):
    "Allow to save all diagram in a the program format."

    def __init__(self, parent, canvas, status):
        pattern = ("pybox Files", "*.pybox")
        name = "untitled.pybox"
        SaveDialog.__init__(self, parent, canvas, status, pattern, name)

    def _save_canvas_to(self, filename):
        file = open(filename, 'wb')
        pickle = cPickle.Pickler(file)

        # TODO: Quitar el nombre de modelo de la lista 'canvas.boxes'.
        boxes = [box for (name, box) in self.canvas.boxes]
        dump = [(box.x, box.y, box.model) for box in boxes]

        #print "Modelo de datos a guardar:"
        #print "\t", dump

        # format: type list = [(x, y, model), ...]
        pickle.dump(dump)
        file.close()
