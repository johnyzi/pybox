# -*- encoding: utf-8 -*-
import os
import time

import common
from dialogs.leave import Leave

class Session:
    """Representa el estado del documento o diagrama.

    Conoce el nombre de documento, cuando se grabó por última vez y que
    archivo de disco representa.
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
        return dialog.run()

    def _set_title(self):
        """Set main window title according to session state."""

        if self.changes_not_saved > 0:
            self.main.set_title("* %s - pybox" %self.name)
        else:
            self.main.set_title("%s - pybox" %self.name)
