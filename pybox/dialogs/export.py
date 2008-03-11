# -*- encoding: utf-8 -*-
import gtk
import cairo

class PNG:
    """Allow to export canvas area in a .PNG file."""

    def __init__(self, parent, canvas, status):
        self.canvas = canvas
        self.parent = parent
        self.status = status
        self._create_dialog()
        self._run()
    
    def _create_dialog(self):
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                gtk.STOCK_SAVE, gtk.RESPONSE_OK)
        action = gtk.FILE_CHOOSER_ACTION_SAVE 

        dialog = gtk.FileChooserDialog(action=action, 
                buttons=buttons,
                parent=self.parent)
        dialog.set_do_overwrite_confirmation(True)

        dialog.set_current_name("untitled.png")

        # Filtro (*.png)
        filter = gtk.FileFilter()
        filter.set_name("PNG Files")
        filter.add_pattern("*.png")
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

    def _save_canvas_to(self, filename):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 600)
        cr = cairo.Context(surface)
        self.canvas.render(cr, None, 1.0)
        cr.show_page()

        try:
            surface.write_to_png(filename)
        except IOError:
            self.status.error("I can't write this file")
            return

        self.status.info("File save in", filename)
