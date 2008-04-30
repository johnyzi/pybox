# -*- encoding: utf-8 -*-
import cPickle
import gtk
import cairo
import goocanvas

class SaveDialog:
    """Abstract save dialog."""

    def __init__(self, parent, canvas, status, pattern, name):
        self.canvas = canvas
        self.parent = parent
        self.status = status
        self._create_dialog(pattern, name)

    def _create_dialog(self, pattern, name):
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                gtk.STOCK_SAVE, gtk.RESPONSE_OK)
        action = gtk.FILE_CHOOSER_ACTION_SAVE 

        dialog = gtk.FileChooserDialog(action=action, 
                buttons=buttons,
                parent=self.parent)
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_name(name)

        # Custom filter
        filter = gtk.FileFilter()
        label, mask = pattern
        filter.set_name(label)
        filter.add_pattern(mask)
        dialog.add_filter(filter)

        # All files filter (*)
        filter = gtk.FileFilter()
        filter.set_name("All Files")
        filter.add_pattern("*")
        dialog.add_filter(filter)
        self.dialog = dialog

    def run(self):
        response = self.dialog.run()
        self.dialog.hide()

        if response == gtk.RESPONSE_OK:
            return self._save_canvas_to(self.dialog.get_filename())
        else:
            return False


class PNG(SaveDialog):
    """Allow to export canvas area in a .PNG file."""

    def __init__(self, parent, canvas, status):
        pattern = ("PNG Files", "*.png")
        name = "%s.png" %(canvas.session.name)
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
        return True


class PDF(SaveDialog):
    """Allow to export canvas area in a .PDF file."""

    def __init__(self, parent, canvas, status):
        pattern = ("PDF Files", "*.pdf")
        name = "%s.pdf" %(canvas.session.name)
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
        return True

class Document(SaveDialog):
    "Allow to save all diagram in a the program format."

    def __init__(self, parent, canvas, status):
        pattern = ("pybox Files", "*.pybox")
        name = "%s.pybox" %(canvas.session.name)
        SaveDialog.__init__(self, parent, canvas, status, pattern, name)

    def _save_canvas_to(self, filename):
        try:
            file = open(filename, 'wb')
        except IOError:
            self.status.error("I can't write the file as %s." %filename)
            return

        pickle = cPickle.Pickler(file)

        dump = [(box.x, box.y, box.model) for box in self.canvas.boxes]

        # format: type list = [(x, y, model), ...]
        pickle.dump(dump)
        file.close()
        self.status.info("File saved as %s" %filename)
        self.canvas.session.save_document_notify(filename)
        return True
