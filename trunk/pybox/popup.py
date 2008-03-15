import gtk
import model
import dialogs

from window import Window

class Popup(Window):
    def __init__(self, canvas):
        Window.__init__(self, 'popup.glade')
        self.canvas = canvas


    def on_add__activate(self, widget):
        "Raise the window to create a new class."
        new_model = model.Model()
        new_dialog = dialogs.classview.ClassView(new_model,
                self.canvas.get_class_names())
        response = new_dialog.view.dialog1.run()

        if response:
            self.canvas.create_box(new_model)

    def on_remove__activate(self, widget):
        self.canvas.remove_selected_box()
        print self.canvas.boxes

    def on_edit__activate(self, widget, box=None):

        if not box:
            box = self.canvas.box

        last_name = box.model.name
        new_dialog = dialogs.classview.ClassView(box.model,
                self.canvas.get_class_names())
        response = new_dialog.view.dialog1.run()

        if response:
            box.update(box.model, last_name)
            self.canvas.connect_box(box, box.model)



    def show(self, event, new):

        self.view.add.set_sensitive(new)
        self.view.edit.set_sensitive(not new)
        self.view.remove.set_sensitive(not new)

        self.view.popup.popup(None, None, None, event.button, event.time)

