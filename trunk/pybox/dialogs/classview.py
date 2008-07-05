# -*- encoding: utf-8 -*-
import gtk
import gtk.glade
import gtk.gdk
import dialogs
import common
import re

from window import Window

NONE_CLASS = "<None>"
NONE_INDEX = 0

class ClassView(Window):
    """Representa las propiedades de una clase de forma visual.

    Se utiliza en dos casos, cuando se quiere crear un nuevo objeto
    y cuando se modifican los datos de una clase existente."""

    def __init__(self, model, classes):
        Window.__init__(self, 'class.glade')
        self.model = model
        self.classes = classes
        self._populate_ui()

        self._change_selection_mode()

        self._create_superclass_list(classes)
        self._select_model_superclass()
        self.load_attributes()

    def _populate_ui(self):
        self.view.accept.set_sensitive(False)
        self.view.addattr.set_sensitive(False)
        self.view.addmethod.set_sensitive(False)
        self.view.name.set_text(self.model.name)
        self.view.abstract.set_active(self.model.abstract)
    
    def _change_selection_mode(self):
        # Permite realizar multiples selecciones sobre el treeview (con shift y ctrl)
        # Allows us to make multiple selections on the treeview.

        treeselection_mode = self.view.treeview_attributes.get_selection()
        treeselection_mode.set_mode(gtk.SELECTION_MULTIPLE)

        treeselection_mode = self.view.treeview_methods.get_selection()
        treeselection_mode.set_mode(gtk.SELECTION_MULTIPLE)

    def _select_model_superclass(self):
        "Set the selected superclass in UI from model class."

        if self.model.superclass:
            if len(self.model.superclass) > 1:
                # Multiple hierarchy
                self._create_superclass_row_and_select_em(self.model.superclass)
            else:
                # Simple Hierarchy
                self._select_single_superclass(self.model.superclass[0])
        else:
            self.view.superclass.set_active(NONE_INDEX)

    def _select_single_superclass(self, name):
        superclass_name = name
        elements_in_combo = [n[0] for n in self.view.superclass.get_model()]
        index = elements_in_combo.index(superclass_name)
        self.view.superclass.set_active(index)

    def _create_superclass_row_and_select_em(self, list_of_classes_to_merge):
        """Creates a new row in superclass combobox and select em."""

        tree_model = self.view.superclass.get_model()
        tree_model.append([common.list_to_string(list_of_classes_to_merge)])
        index = len(tree_model) - 1
        self.view.superclass.set_active(index)

    def _create_superclass_list(self, classes):
        """Creates a combobox to select a superclass for a class model."""
        store = gtk.ListStore(str)

        store.append([NONE_CLASS])

        for name in classes:
            if name != self.model.name:
                store.append([name])

        combo = self.view.superclass
        combo.set_model(store)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)
        combo.set_active(0)

        # Solo permite elegir superclase en caso de tener disponibilidad.
        self.view.classlist.set_sensitive(False)

        if len(store) > 1:
            combo.set_sensitive(True)
            if len(store) > 2:
                self.view.classlist.set_sensitive(True)
        else:
            combo.set_sensitive(False)

    def load_attributes(self):
        """Creates both methods and variables treeviews."""

        # Armamos el treeview de los atributos.
        # We build the attribute treeview

        attribute_column = gtk.TreeViewColumn('Atributtes', gtk.CellRendererText(), 
                text=0)
        self.view.treeview_attributes.append_column(attribute_column)
        attribute_model = gtk.ListStore(str)

        for item in self.model.variables:
            attribute_model.append([item])

        self.view.treeview_attributes.set_model(attribute_model)

        # Armamos el treeview de los metodos.
        # We build the method treeview.

        method_column = gtk.TreeViewColumn('Methods', gtk.CellRendererText(), 
                text=0)
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

    def check_syntax(self, string_to_chk, reg_exp, error_msg, hbox,
            label_widget, entry_widget, ok_button):
        reg_ex = re.compile(reg_exp)
            
        if not reg_ex.match(string_to_chk):
            if len(string_to_chk) :
                ok_button.set_sensitive(False)
                label_widget.set_markup(error_msg)
                hbox.show()

                entry_widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFDDDD'))
                #print "Entre en MOSTRAR."

                return True
        else:
            hbox.hide()
            entry_widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
            #print "Entre en OCULTAR."

            return False

    def check_duplicated(self, string_to_chk, treeview, error_msg, hbox,
            label_widget, entry_widget, ok_button):
        
        elements = treeview.get_model()
        variables = [name[0] for name in elements]

        if string_to_chk in variables:
            ok_button.set_sensitive(False)
            label_widget.set_markup(error_msg)
            hbox.show()
            entry_widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFDDDD'))

            return True

        else:
            hbox.hide()
            label_widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))

            return False

    def on_attrentry__changed(self, widget):
        if len(self.view.attrentry.get_text()) > 0:
            self.view.addattr.set_sensitive(True)
        else:
            self.view.addattr.set_sensitive(False)
            #self.view.error.hide()

        # validacion
        entry_text = self.view.attrentry.get_text()

        if self.check_syntax(entry_text, "^([a-z,A-Z,_]+\d*)+$", "<i>Invalid attribute name.</i>", self.view.error,
                self.view.attrentry_error, self.view.attrentry, self.view.addattr):
            return
        
        if self.check_duplicated(entry_text,
                self.view.treeview_attributes, "<i>Attribute already defined.</i>", self.view.error, self.view.attrentry_error, self.view.attrentry,
                self.view.addattr):
            return

    def on_methodentry__changed(self, widget):
        if len(self.view.methodentry.get_text()) > 0:
            self.view.addmethod.set_sensitive(True)
        else:
            self.view.addmethod.set_sensitive(False)
            #self.view.hbox_method_error.hide()

        entry_text = self.view.methodentry.get_text()

        if self.check_syntax(entry_text, "^([a-z,A-Z,_]+[\d,\(,\),\,,\;\:\ \"\'\=]*)+$", "<i>Invalid method name.</i>", 
                self.view.hbox_method_error, self.view.methodentry_error, self.view.methodentry,
                self.view.addmethod):
            return

        if self.check_duplicated(entry_text,
                self.view.treeview_methods, "<i>Method already defined.</i>", self.view.hbox_method_error, self.view.methodentry_error,
                self.view.methodentry, self.view.addmethod):
            return
    
    def on_attrentry__activate(self, widget):
        state = self.view.addattr.get_property('sensitive')

        if state:
            self.on_addattr__clicked(widget)

    def on_methodentry__activate(self, widget):
        state = self.view.addmethod.get_property('sensitive')

        if state:
            self.on_addmethod__clicked(widget)

    def on_accept__clicked(self, widget):
        #print "Nombre anterior:", self.model.name
        self.model.name = self.view.name.get_text()
        #print "Nombre nuevo:", self.model.name
        
        #TODO
        ''' para probar a superclasss como lista hago que el único string
        seleccionado pase a ser una lista de un elemento'''
        #superclass = [self.view.superclass.get_active_text()]
        selected_classes = self.view.superclass.get_active_text()

        if selected_classes != NONE_CLASS:
            self.model.superclass = common.string_to_list(selected_classes)
        else:
            self.model.superclass = []

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

    def on_classlist__clicked(self, widget):
        current_superclass = self.view.superclass.get_active_text()

        if current_superclass == NONE_CLASS:
            selected_class = []
        else:
            selected_class = common.string_to_list(current_superclass)
            
        classes = [name for name in self.classes if name != self.model.name]

        dialog = dialogs.classlist.ClassList(classes, selected_class)
        selected_classes = dialog.run()

        if selected_classes is not None:
            if len(selected_classes) > 1:
                self._create_superclass_row_and_select_em(selected_classes)
            elif len(selected_classes) == 1:
                self._select_single_superclass(selected_classes[0])
            else:
                self.view.superclass.set_active(NONE_INDEX)
