# -*- encoding: utf-8 -*-
import gtk
import gtk.glade
import goocanvas

import dialogs
import model
import canvas

from window import Window

class Main(Window):
    """ 
    Ventana Principal del programa
    """
    
    def __init__(self):
        Window.__init__(self, 'main.glade')
        self.view.main.show()
        self.canvas = canvas.Canvas(self)
        self.view.scroll.add(self.canvas)

    def on_quit_item__activate(self, widget):
        self.on_main__destroy(widget)

    def on_main__destroy(self, widget):
        gtk.main_quit()

'''    # Al presionar sobre el boton 'Add' del menu desplegamos la ventana para crear una nueva clase.
    # When the 'Add' button is pressed we raise the window to create a new class.

    def on_add__activate(self, widget):
        new_model = model.Model()
        new_dialog = dialogs.classview.ClassView(new_model, self.canvas.classes)
        response = new_dialog.view.dialog1.run()

        if response:
            self.canvas.create_box(new_model)

    def on_remove__activate(self, widget):
        self.canvas.remove_selected_box()


    def on_edit__activate(self, widget):
        new_dialog = dialogs.classview.ClassView(self.canvas.box.model,
                self.canvas.classes)
        response = new_dialog.view.dialog1.run()

        if response:
            self.canvas.box.update(self.canvas.box.model)'''


if __name__ == '__main__':
    main = Main()
    gtk.main()
