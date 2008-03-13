import cPickle
import gtk

class OpenDialog:
    def __init__(self, parent, canvas, status, pattern, name):
        self.canvas = canvas
        self.parent = parent
        self.status = status
        self._create_dialog(pattern, name)
        self._run()

    def _create_dialog(self, pattern, name):
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        action = gtk.FILE_CHOOSER_ACTION_OPEN 

        dialog = gtk.FileChooserDialog(action=action, 
                buttons=buttons,
                parent=self.parent)
        dialog.set_do_overwrite_confirmation(True)


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
            self._open(self.dialog.get_filename())

        self.dialog.hide()

class Document(OpenDialog):
    "Allow to save all diagram in a the program format."

    def __init__(self, parent, canvas, status):
        pattern = ("pybox Files", "*.pybox")
        name = "untitled.pybox"
        OpenDialog.__init__(self, parent, canvas, status, pattern, name)

    def _open(self, filename):
        file = open('project.pybox', 'rb')
        dump = cPickle.load(file)

        self.canvas.clear()

        for (x, y, model) in dump:
            self.canvas.create_box(model, x, y, hierarchy_lines=False)

        # Connect lines
        # TODO: Quitar el nombre de modelo de la lista Canvas.boxes
        for (name, box) in self.canvas.boxes:
            self.canvas.connect_box(box, box.model)
