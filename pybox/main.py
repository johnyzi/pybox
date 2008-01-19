
# -*- encoding: utf-8 -*-
import gtk
import gtk.glade

from window import Window

class Main(Window):
    """ 
    Ventana Principal del programa
    """
    
    def __init__(self):
        Window.__init__(self, 'main.glade')
        self.view.main.show()
    
    
if __name__ == '__main__':
    main = Main()
    gtk.main()

    

