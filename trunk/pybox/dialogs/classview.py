    # -*- encoding: utf-8 -*-
import gtk
import gtk.glade

from window import Window

NONE_CLASS = "<None>"

class ClassView(Window):
    """Representa las propiedades de una clase de forma visual.

    Se utiliza en dos casos, cuando se quiere crear un nuevo objeto
    y cuando se modifican los datos de una clase existente."""

    def __init__(self, model, classes):
        model.show()
        Window.__init__(self, 'class.glade')
        self.view.accept.set_sensitive(False)
        self.view.addattr.set_sensitive(False)
        self.view.addmethod.set_sensitive(False)
        self.model = model
        self.view.name.set_text(model.name)
        #self.view.superclass.set_active(model.superclass)
        self.view.abstract.set_active(model.abstract)

        # Permite realizar multiples selecciones sobre el treeview (con shift y ctrl)
        # Allows us to make multiple selections on the treeview.

        treeselection_mode = self.view.treeview_attributes.get_selection()
        treeselection_mode.set_mode(gtk.SELECTION_MULTIPLE)

        treeselection_mode = self.view.treeview_methods.get_selection()
        treeselection_mode.set_mode(gtk.SELECTION_MULTIPLE)

        self._create_superclass_list(classes)

        if model.superclass:
            list = [n[0] for n in self.view.superclass.get_model()]
            try:
                self.view.superclass.set_active(list.index(model.superclass))
            except:
                print "Ups!, la superclase de este modelo se ha borrado."

        self.load_attributes()

    def _create_superclass_list(self, classes):
        store = gtk.ListStore(str)

        store.append([NONE_CLASS])

        for model in classes:
            if model.name != self.model.name:
                store.append([model.name])

        combo = self.view.superclass
        combo.set_model(store)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)
        combo.set_active(0)

    def load_attributes(self):
        # Armamos el treeview de los atributos.
        # We build the attribute treeview

        attribute_column = gtk.TreeViewColumn('Atributtes', gtk.CellRendererText(), text = 0)
        self.view.treeview_attributes.append_column(attribute_column)
        attribute_model = gtk.ListStore(str)

        for item in self.model.variables:
            attribute_model.append([item])

        self.view.treeview_attributes.set_model(attribute_model)

        # Armamos el treeview de los metodos.
        # We build the method treeview.

        method_column = gtk.TreeViewColumn('Methods', gtk.CellRendererText(), text = 0)
        self.view.treeview_methods.append_column(method_column)
        method_model= gtk.ListStore(str)
        
        for item in self.model.methods:
            method_model.append([item])

        self.view.treeview_methods.set_model(method_model)

    def on_dialog1__delete_event(self, widget, extra):
        self.view.dialog1.response(0)
        self.view.dialog1.destroy()
    
    def on_name__changed(self, widget):
        # Si se escribe el nombre de la clase entonces permitimos que el usuario pueda presionar OK para crearla.
        # If the name of the class is written then we allow the user to create the class.

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

    def on_attrentry__activate(self, widget):
        if len(self.view.attrentry.get_text()) > 0:
            self.on_addattr__clicked(widget)

    def on_methodentry__activate(self, widget):
        if len(self.view.methodentry.get_text()) > 0:
            self.on_addmethod__clicked(widget)

    def on_accept__clicked(self, widget):
        self.model.name = self.view.name.get_text()
        superclass = self.view.superclass.get_active_text()

        if superclass and superclass != NONE_CLASS:
            self.model.superclass = superclass
        else:
            self.model.superclass = ""

        self.model.abstract = self.view.abstract.get_active()

        model_attributes = self.view.treeview_attributes.get_model()
        self.model.variables = [name[0] for name in model_attributes]

        model_methods = self.view.treeview_methods.get_model()
        self.model.methods = [name[0] for name in model_methods]

        
        # Al presionar OK, cerramos la ventana.
        # When we press OK we close the window.
        self.view.dialog1.destroy()

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
        self.view.attrentry.set_text('')

    def on_addmethod__clicked(self, widget):
        model = self.view.treeview_methods.get_model()
        model.append([self.view.methodentry.get_text()])
        self.view.treeview_methods.set_model(model)
        self.view.methodentry.set_text('')

