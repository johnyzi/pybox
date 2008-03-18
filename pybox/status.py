# -*- encoding: utf-8 -*-
import gtk
import re
import config
import dialogs

class StatusBar(gtk.EventBox):
    """Muestra los mensajes de estado del programa.

    StatusBar funciona en reemplazo del widget StatusBar de GTK, añadiendo
    un icono de notificación y varios métodos para facilitar la iteracción
    con el resto del programa.

    Ejemplo de uso:
        
        bar = StatusBar()
        window.add(bar)

        bar.info('Program started', 'Now you can use this program')
        gtk.main()
    """

    def __init__(self, main):
        gtk.EventBox.__init__(self)
        self.ui = gtk.glade.XML('statusbar.glade')
        self.image = self.ui.get_widget('image')
        self.status = self.ui.get_widget('status')
        vbox = self.ui.get_widget("vbox1")
        vbox.reparent(self)
        self.set_border_width(3)
        self.clear()
        self.show()

        if config.DEBUG:
            debug = self.ui.get_widget('debug')
            debug.connect('clicked', self._show_debugger, main)
            debug.show()

    def warning(self, message, long=None):
        self._set_message(gtk.STOCK_DIALOG_WARNING, message, long)

    def error(self, message, long=None):
        self._set_message(gtk.STOCK_DIALOG_ERROR, message, long)

    def info(self, message, long=None):
        self._set_message(gtk.STOCK_DIALOG_INFO, message, long)

    def clear(self):
        self.image.hide()
        self.status.set_text("")

    def _set_message(self, stock_item, message, long):
        self.image.show()
        self.image.set_from_stock(stock_item, gtk.ICON_SIZE_SMALL_TOOLBAR)

        if long:
            self.status.set_text(" " + message + "...")
            self.status.set_tooltip_markup(long)
        else:
            self.status.set_text(" " + message)

    def _show_debugger(self, widget, main):
        debugger = dialogs.debugger.Debugger(main.view.main, main)
        debugger.run()
