# -*- encoding: utf-8 -*-
import gtk
import gtk.glade
from window import Window

class ClassList(Window):
    """Show a multiple seleccion list of classes."""

    def __init__(self, classes, selected_classes):
        """
        Params:
            `classes`: list of strings with all class names.
            `selected_classes`: list of strings with selected classes.
        """
        Window.__init__(self, 'classlist.glade')
        self._create_list()
        self._populate_model(classes, selected_classes)
        self.view.classlist.set_default_size(300, 300)

    def _create_list(self):
        self.model = gtk.ListStore(bool, str)

        # Column 0 (Select)
        cell = gtk.CellRendererToggle()
        cell.set_property("activatable", True)
        cell.connect('toggled', self._on_toggle)
        check = gtk.TreeViewColumn('Select', cell, active=0)

        # Column 1 (Name)
        name = gtk.TreeViewColumn('Name', gtk.CellRendererText(), text=1)

        # Append Columns
        self.view.treeview.append_column(check)
        self.view.treeview.append_column(name)

        self.view.treeview.set_model(self.model)

    def _populate_model(self, classes, selected_classes):
        # Populate model
        for name in classes:
            is_selected = name in selected_classes
            self.model.append((is_selected, name)) 

    def _on_toggle(self, widget, index):
        self.model[index][0] = not self.model[index][0]

    def run(self):
        """Show the class lists.

        Return:
            A list of selected class names or None if user select cancel.
        """
        response = self.view.classlist.run()
        self.view.classlist.hide()

        if response == 2:
            return [name for (state, name) in self.model if state]
