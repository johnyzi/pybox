import gtk
import model
import dialogs

from window import Window

class Popup(Window):
    def __init__(self, canvas):
        Window.__init__(self, 'popup.glade')
        self.canvas = canvas

    # Al presionar sobre el boton 'Add' del menu desplegamos la ventana para crear una nueva clase.
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
            self.canvas.box.update(self.canvas.box.model)

    def show(self, event, new):

        self.view.add.set_sensitive(new)
        self.view.edit.set_sensitive(not new)
        self.view.remove.set_sensitive(not new)

        self.view.popup.popup(None, None, None, event.button, event.time)

