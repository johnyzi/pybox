# -*- encoding: utf-8 -*-
import os
import time

import common
from dialogs.leave import Leave

class Session:
    """Representa el estado del documento o diagrama.

    Todos los componentes del sistema notifican a este objeto la acción
    solicitada por el usuario, los métodos que reciben estas notificaciones
    tienen la forma "on_notify_#" donde # puede ser "edit_class", "redo" etc.

    Este objeto conoce el nombre de documento, cuando se grabó por última vez
    y que archivo de disco representa. 
    """

    def __init__(self, main):
        self.main = main
        self.new_document_notify()

    def new_document_notify(self):
        self.name = 'Untitled'
        self._clear_state()
        self.main.set_can_export(False)

    def open_document_notify(self, filename):
        self.name = common.get_filename_without_extension(filename)
        self._clear_state()

    def save_document_notify(self, filename):
        self.name = common.get_filename_without_extension(filename)
        self._clear_state()

    def change_notify(self):
        self.changes_not_saved += 1
        self._set_title()
        self.main.set_can_save(True)
        self.main.set_can_export(True)

    def can_leave(self, save_callback):
        "Try to leave this session; if it is't possible show a confirm dialog."""

        if self.changes_not_saved > 0:
            return self._show_confirm_dialog(save_callback)
        else:
            return True

    def _clear_state(self):
        self.last_save_time = time.time()
        self.changes_not_saved = 0
        self._set_title()
        self.main.set_can_save(False)

    def _show_confirm_dialog(self, save_callback):
        dialog = Leave(self.name, self.changes_not_saved, self.last_save_time, 
                save_callback)
        response = dialog.run()
        print "Dialog.run devuelve", response
        return response

    def _set_title(self):
        """Set main window title according to session state."""

        if self.changes_not_saved > 0:
            self.main.set_title("* %s - pybox" %self.name)
        else:
            self.main.set_title("%s - pybox" %self.name)



    # Eventos de aplicación
    # =====================

    def on_notify_create_class(self, model):
        print "Session:notify - Se ha creado la clase:", model
        self.main.history.push_undo('BOX_CREATED')
        self.main.view.status.info("Creating <b>%s</b> class" %(model.name))
        self.change_notify()

    def on_notify_move_class(self, model):
        print "Session:notify - Se ha movido una caja llamada:", model
        self.main.view.status.info("Moving <b>%s</b> class box" %(model.name))
        self.main.history.push_undo('BOX_MOVED')
        self.change_notify()

    def on_notify_undo(self):
        print "Session:notify - Se ha invocado al método undo."
        self.main.history.pop_undo()

    def on_notify_redo(self):
        print "Session:notify - Se ha invocado al método redo."
        self.main.history.pop_redo()

    def on_notify_edit_class(self, model, last_name):
        print "Session:notify - Se ha modificado una clase de modelo:", model
        print "asdadsasdasdasd"

        if model.name != last_name:
            msg = "Editing <b>%s</b> class (that was called <b>%s</b> class)" %(model.name, last_name)
            self.main.view.status.info(msg)
        else:
            self.main.view.status.info("Editing <b>%s</b> class" %(model.name))

    def on_notify_remove_class(self, model):
        print "Session:notify - Se elimina una caja de modelo:", model
        self.main.view.status.info("Removing <b>%s</b> class" %(model.name))
        self.main.history.push_undo('BOX_REMOVED')
        self.change_notify()
