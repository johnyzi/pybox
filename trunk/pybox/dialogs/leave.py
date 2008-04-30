# -*- encoding: utf-8 -*-
from window import Window
import time

class Leave(Window):
    "Consulta al usuario si desea guardar los cambios del documento."

    def __init__(self, name, changes, time_last_save, save_callback):
        Window.__init__(self, 'leave.glade')
        self.can_continue = False
        self.save_callback = save_callback
        self._populate_template(name, changes, time_last_save)

    def _populate_template(self, name, changes, time_last_save):
        name_template = self.view.msg_1.get_text()
        name_text = name_template.replace("NAME", name)
        self.view.msg_1.set_markup("<b>" + name_text + "</b>")

        long_template = self.view.msg_2.get_text()
        minutes = int((time.time() - time_last_save) / 60.0)
        
        #HACK: Buscar otra forma de llenar un patrón.
        v1 = ("NUMBER", str(changes))
        v2 = ("MINUTES", str(minutes))
        long_text = long_template.replace(*v1).replace(*v2)
        self.view.msg_2.set_text(long_text)

    def on_save__clicked(self, widget):
        self.can_continue = self.save_callback(widget)

    def on_discard__clicked(self, widget):
        self.can_continue = True

    def on_cancel__clicked(self, widget):
        self.can_continue = False

    def run(self):
        """Returns True if it posible to continue or False if user cancel."""
        self.view.leave.run()
        self.view.leave.hide()
        return self.can_continue
