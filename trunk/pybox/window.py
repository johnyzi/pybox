# -*- encoding: utf-8 -*-
import gtk
import gtk.glade
import re

class View:
    pass

class Window:
    """Representa el comportamiento de una ventana gráfica.

    Se encarga de autoconectar señales, asociar los elementos de la 
    interfaz como atributos y cargar el archivo glade."""

    def __init__(self, ui_file):
	self.ui = gtk.glade.XML(ui_file)
	self._connect_callbacks(self.ui)
	self._create_view(self.ui)

    def _connect_callbacks(self, ui):
        "Intenta auto-conectar todos los manejadores de señal."

        expresion = re.compile("on_(.*)__(.*)")

        methods_list = [x for x in dir(self) if expresion.match(x)]

        for method in methods_list:
            result = expresion.search(method)
            widget_name = result.group(1)
            signal = result.group(2)

            widget = ui.get_widget(widget_name)
            function = getattr(self, method)
            widget.connect(signal, function)

    def _create_view(self, ui):
        widgets_list = ui.get_widget_prefix("")
        self.view = View()

        for widget in widgets_list:
            name = widget.name
            setattr(self.view, name, widget)
