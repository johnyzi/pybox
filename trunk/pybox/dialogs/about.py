# -*- encoding: utf-8 -*-
import gtk
import common

class About:
    """Show some information about developers and software license."""

    def __init__(self):
        image = gtk.Image()
        dialog = gtk.AboutDialog()
        dialog.set_name("Pybox")
        dialog.set_comments("A simple class diagram tool.")
        dialog.set_license(common.GPL_TEXT)
        dialog.set_authors(common.AUTHORS)
        image.set_from_file("../pixmaps/logo.png")
        dialog.set_logo(image.get_pixbuf())
        self.dialog = dialog

    def run(self):
        self.dialog.run()
        self.dialog.hide()
