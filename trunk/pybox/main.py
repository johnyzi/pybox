# -*- encoding: utf-8 -*-
import gtk
import gtk.glade
import goocanvas

import common
import dialogs
import model
import canvas
import status
import dialogs.save
import config
import history

from window import Window

class Main(Window):
    """ 
    Representa la ventana Principal del programa.

    Este objeto gestiona los manejadores de señal de la barra de herramientas
    y el menú superior de la ventana.
    """
    
    def __init__(self):
        Window.__init__(self, 'main.glade')
        self._create_canvas()
        self._create_status_bar()
        self._create_history()
        self.view.main.show()

    def set_title(self, string):
        "Define el título de la ventana."
        self.view.main.set_title(string)

    def set_can_save(self, state):
        "Define si habilita o no la posibilidad de guardar."
        self.view.saveas.set_sensitive(state)
        self.view.new.set_sensitive(state)
        self.view.new_button.set_sensitive(state)

    def set_can_export(self, state):
        "Define si habilita o no la posibilidad de exportar el documento."
        self.view.saveas.set_sensitive(state)
        self.view.export_png_item.set_sensitive(state)
        self.view.export_pdf_item.set_sensitive(state)

    def _create_canvas(self):
        "Construye el area de dibujo."
        self.canvas = canvas.Canvas(self)
        self.view.scroll.add(self.canvas)

    def _create_history(self):
        "Construye el historial de cambios (deshacer y reahacer)."
        self.history = history.History(self)

    def _create_status_bar(self):
        "Construye la barra de notificaciones."
        self.view.status = status.StatusBar(self)
        self.view.status_placeholder.add(self.view.status)
        self.view.status.info("Starting program")

    # Manejadores de señal

    def on_main__destroy(self, widget):
        gtk.main_quit()

    
    def on_new__activate(self, widget):
        self.canvas.new()

    def on_quit_item__activate(self, widget):
        self.on_main__delete_event(widget)

    def on_setup_item__activate(self, widget):
        dialog = dialogs.settings.Settings()
        dialog.run()

    def on_main__delete_event(self, widget, extra=None):
        if not config.DEBUG:
            if self.canvas.show_confirm_save_dialog():
                gtk.main_quit()
        else:
            gtk.main_quit()
            print "* Se cierra sin confirmar a causa de la constante DEBUG=True."


    def on_export_png_item__activate(self, widget):
        dialogs.save.PNG(self.view.main, self.canvas, self.view.status)

    def on_export_pdf_item__activate(self, widget):
        dialogs.save.PDF(self.view.main, self.canvas, self.view.status)

    def on_saveas__activate(self, widget):
        self.canvas.save_as()

    def on_open__activate(self, widget):
        self.canvas.open_dialog()

    def on_undo_item__activate(self, widget):
        self.canvas.session.on_notify_undo()

    def on_redo_item__activate(self, widget):
        self.canvas.session.on_notify_redo()

    def on_aboutitem__activate(self, item):
        dialog = dialogs.about.About()
        self.view.status.info("Showing about dialog")
        dialog.run()
        self.view.status.info("About dialog has closed")

    # Barra de botones

    def on_new_button__clicked(self, widget):
        self.on_new__activate(widget)

    def on_undo_button__clicked(self, widget):
        self.on_undo__activate(widget)

    def on_redo_button__clicked(self, widget):
        self.on_redo__activate(widget)

if __name__ == '__main__':
    main = Main()
    gtk.main()
