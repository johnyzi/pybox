# -*- encoding: utf-8 -*-
import gtk
import gtk.glade

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
        self.view.main.set_size_request(450, 300)
        self.view.main.show()

    def set_title(self, string):
        "Define el título de la ventana."
        self.view.main.set_title(string)

    def set_can_save(self, state):
        "Define si habilita o no la posibilidad de guardar."
        self.view.saveas.set_sensitive(state)
        #self.view.new.set_sensitive(state)
        #self.view.new_button.set_sensitive(state)

    def set_can_export(self, state):
        "Define si habilita o no la posibilidad de exportar el documento."
        self.view.saveas.set_sensitive(state)
        self.view.export_png_item.set_sensitive(state)
        self.view.export_svg_item.set_sensitive(state)
        self.view.export_pdf_item.set_sensitive(state)

    def _create_canvas(self):
        "Construye el area de dibujo."
        self.canvas = canvas.Canvas(self)
        self.view.canvas_placeholder.add(self.canvas)

        self.canvas.set_size_request(150, 120)
        self.view.hscrollbar.set_adjustment(self.canvas.hadjustment)
        self.view.vscrollbar.set_adjustment(self.canvas.vadjustment)


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
        self.canvas.show_create_class_dialog()

    def on_quit_item__activate(self, widget):
        self.on_main__delete_event(widget)

    def on_setup_item__activate(self, widget):
        self.view.status.info("Showing settings dialog")
        dialog = dialogs.settings.Settings()
        dialog.run()
        self.view.status.info("Setting dialog was closed")

    def on_main__delete_event(self, widget, extra=None):
        if not config.DEBUG:
            if self.canvas.show_confirm_save_dialog():
                gtk.main_quit()
            else:
                return True
        else:
            gtk.main_quit()

    def on_export_png_item__activate(self, widget):
        d = dialogs.save.PNG(self.view.main, self.canvas, self.view.status)
        d.run()

    def on_export_svg_item__activate(self, widget):
        d = dialogs.save.SVG(self.view.main, self.canvas, self.view.status)
        d.run()

    def on_export_pdf_item__activate(self, widget):
        d = dialogs.save.PDF(self.view.main, self.canvas, self.view.status)
        d.run()

    def on_saveas__activate(self, widget):
        self.canvas.save_as()

    def on_open__activate(self, widget):
        if self.canvas.show_confirm_save_dialog():
            self.canvas.open_dialog()

    def on_undo_item__activate(self, widget):
        self.canvas.session.on_notify_undo()

    def on_redo_item__activate(self, widget):
        self.canvas.session.on_notify_redo()

    def on_aboutitem__activate(self, item):
        dialog = dialogs.about.About()
        self.view.status.info("Showing about dialog")
        dialog.run()
        self.view.status.info("About dialog was closed")

    # Barra de botones

    def on_new_button__clicked(self, widget):
        self.on_new__activate(widget)

    def on_undo_button__clicked(self, widget):
        self.on_undo_item__activate(widget)

    def on_redo_button__clicked(self, widget):
        self.on_redo_item__activate(widget)

    def on_zoomin_button__clicked(self, widget):
        self.canvas.zoom_in()

    def on_zoomout_button__clicked(self, widget):
        self.canvas.zoom_out()


if __name__ == '__main__':
    main = Main()
    gtk.main()
