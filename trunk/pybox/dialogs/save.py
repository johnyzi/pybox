# -*- encoding: utf-8 -*-
import cPickle
import gtk
import cairo
import gaphas

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
        svgview = gaphas.View(self.canvas.canvas)
        svgview.painter = gaphas.painter.ItemPainter()

        tmpsurface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
        tmpcr = cairo.Context(tmpsurface)
        svgview.update_bounding_box(tmpcr)
        tmpcr.show_page()
        tmpsurface.flush()

        w, h = svgview.bounding_box.width, svgview.bounding_box.height
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w), int(h))

        cr = cairo.Context(surface)
        svgview.matrix.translate(-svgview.bounding_box.x, -svgview.bounding_box.y)
        cr.save()
        svgview.paint(cr)

        cr.restore()
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
        svgview = gaphas.View(self.canvas.canvas)
        svgview.painter = gaphas.painter.ItemPainter()

        tmpsurface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
        tmpcr = cairo.Context(tmpsurface)
        svgview.update_bounding_box(tmpcr)
        tmpcr.show_page()
        tmpsurface.flush()

        w, h = svgview.bounding_box.width, svgview.bounding_box.height

        try:
            surface = cairo.PDFSurface(filename, w, h)
        except IOError:
            self.status.error("I can't write the file as %s." %filename)

        cr = cairo.Context(surface)
        svgview.matrix.translate(-svgview.bounding_box.x, 
                -svgview.bounding_box.y)
        svgview.paint(cr)
        cr.show_page()
        surface.flush()
        surface.finish()

        self.status.info("File saved as %s" %filename)
        return True

class SVG(SaveDialog):
    """Allow to export canvas area in a .SVG file."""

    def __init__(self, parent, canvas, status):
        pattern = ("SVG Files", "*.svg")
        name = "%s.svg" %(canvas.session.name)
        SaveDialog.__init__(self, parent, canvas, status, pattern, name)

    def _save_canvas_to(self, filename):
        svgview = gaphas.View(self.canvas.canvas)
        svgview.painter = gaphas.painter.ItemPainter()

        tmpsurface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
        tmpcr = cairo.Context(tmpsurface)
        svgview.update_bounding_box(tmpcr)
        tmpcr.show_page()
        tmpsurface.flush()

        w, h = svgview.bounding_box.width, svgview.bounding_box.height

        try:
            surface = cairo.SVGSurface(filename, w, h)
        except IOError:
            self.status.error("I can't write the file as %s." %filename)

        cr = cairo.Context(surface)
        svgview.matrix.translate(-svgview.bounding_box.x, 
                -svgview.bounding_box.y)
        svgview.paint(cr)
        cr.show_page()
        surface.flush()
        surface.finish()


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
