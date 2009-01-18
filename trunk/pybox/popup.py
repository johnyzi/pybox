import gtk

from window import Window

class Popup(Window):

    def __init__(self, canvas):
        Window.__init__(self, 'popup.glade')
        self.canvas = canvas
        self.session = canvas.session

    def on_add__activate(self, widget):
        "Raise the window to create a new class."
        self.canvas.show_create_class_dialog()

    def on_remove__activate(self, widget):
        self.canvas.remove_selected_box()

    def on_edit__activate(self, widget, box=None):
        if not box:
            box = self.canvas.box

        last_name = box.model.name
        all_classes = self.canvas.get_class_names()
        new_dialog = dialogs.classview.ClassView(box.model, all_classes)
        response = new_dialog.view.dialog1.run()

        if response:
            box.update(box.model, last_name)
            self.canvas.connect_box(box, box.model)
            self.canvas.session.on_notify_edit_class(box.model, last_name)


    def on_undo__activate(self, widget):
        self.session.on_notify_undo()

    def on_redo__activate(self, widget):
        self.session.on_notify_redo()
        #canvas.history.pop_redo()

    def show(self, event, new):
        self.view.add.set_sensitive(new)
        self.view.edit.set_sensitive(not new)
        self.view.remove.set_sensitive(not new)
        self.view.popup.popup(None, None, None, event.button, event.time)
