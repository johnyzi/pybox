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
        self.model = model
        self.view.name.set_text(model.name)
        self.view.abstract.set_active(model.abstract)
        self.load_attributes()

    def load_attributes(self):
        attribute_column = gtk.TreeViewColumn('Atributos',
                gtk.CellRendererText(), text = 0)
        self.view.treeview_attributes.append_column(attribute_column)
        model = gtk.ListStore(str)

        for item in self.model.variables:
            model.append([item])

        self.view.treeview_attributes.set_model(model)
    
    def on_name__changed(self, widget):
        if len(self.view.name.get_text()) > 0:
            self.view.accept.set_sensitive(True)
        else :
            self.view.accept.set_sensitive(False)
    
    def on_accept__clicked(self, widget):
        self.model.name = self.view.name.get_text()
        self.model.abstract = self.view.abstract.get_active()
        self.model.show()
            
        
        #print self.view.comment_class.get_buffer().get_text()

        
