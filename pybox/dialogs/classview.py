    # -*- encoding: utf-8 -*-
import gtk
import gtk.glade

from window import Window

class ClassView(Window):
    """Representa las propiedades de una clase de forma visual.

    Se utiliza en dos casos, cuando se quiere crear un nuevo objeto
    y cuando se modifican los datos de una clase existente."""

    def __init__(self, model):
        model.show()
        Window.__init__(self, 'class.glade')
        self.view.accept.set_sensitive(False)
        self.view.addattr.set_sensitive(False)
        self.view.addmethod.set_sensitive(False)
        self.model = model
        self.view.name.set_text(model.name)
        self.view.abstract.set_active(model.abstract)

        # Permite realizar multiples selecciones sobre el treeview
        # (con shift y ctrl)

        treeselection_mode = self.view.treeview_attributes.get_selection()
        treeselection_mode.set_mode(gtk.SELECTION_MULTIPLE)

        treeselection_mode = self.view.treeview_methods.get_selection()
        treeselection_mode.set_mode(gtk.SELECTION_MULTIPLE)

        self.load_attributes()

    def load_attributes(self):
        # Armamos el treeview de los atributos.

        attribute_column = gtk.TreeViewColumn('Atributtes', gtk.CellRendererText(), text = 0)
        self.view.treeview_attributes.append_column(attribute_column)
        attribute_model = gtk.ListStore(str)

        for item in self.model.variables:
            attribute_model.append([item])

        self.view.treeview_attributes.set_model(attribute_model)

        # Armamos el treeview de los metodos.

        method_column = gtk.TreeViewColumn('Methods', gtk.CellRendererText(), text = 0)
        self.view.treeview_methods.append_column(method_column)
        method_model= gtk.ListStore(str)
        
        for item in self.model.methods:
            method_model.append([item])

        self.view.treeview_methods.set_model(method_model)
    
    def on_name__changed(self, widget):
        if len(self.view.name.get_text()) > 0:
            self.view.accept.set_sensitive(True)
        else:
            self.view.accept.set_sensitive(False)

    def on_attrentry__changed(self, widget):
        if len(self.view.attrentry.get_text()) > 0:
            self.view.addattr.set_sensitive(True)
        else:
            self.view.addattr.set_sensitive(False)

    def on_methodentry__changed(self, widget):
        if len(self.view.methodentry.get_text()) > 0:
            self.view.addmethod.set_sensitive(True)
        else:
            self.view.addmethod.set_sensitive(False)

    def on_accept__clicked(self, widget):
        self.model.name = self.view.name.get_text()
        self.model.abstract = self.view.abstract.get_active()

        model_attributes = self.view.treeview_attributes.get_model()
        self.model.variables = [name[0] for name in model_attributes]

        model_methods = self.view.treeview_methods.get_model()
        self.model.methods = [name[0] for name in model_methods]

	self.model.show() # Debugging.
        
        # Al presionar OK, cerramos la ventana y devolvemos el modelo.
        self.view.dialog1.destroy()
        return self.model

    def on_cancel__clicked(self, widget):
        self.view.dialog1.destroy()

    def on_removeattr__clicked(self, widget):
        treeview_selection = self.view.treeview_attributes.get_selection()
        model, selected_rows = treeview_selection.get_selected_rows()
        iters = [model.get_iter(path) for path in selected_rows]

        for iter in iters:
            model.remove(iter)

    def on_removemethod__clicked(self, widget):
        treeview_selection = self.view.treeview_methods.get_selection()
        model, selected_rows = treeview_selection.get_selected_rows()
        iters = [model.get_iter(path) for path in selected_rows]

        for iter in iters:
            model.remove(iter)

    def on_addattr__clicked(self, widget):
        model = self.view.treeview_attributes.get_model()
        model.append([self.view.attrentry.get_text()])
        self.view.treeview_attributes.set_model(model)

    def on_addmethod__clicked(self, widget):
        model = self.view.treeview_methods.get_model()
        model.append([self.view.methodentry.get_text()])
        self.view.treeview_methods.set_model(model)

