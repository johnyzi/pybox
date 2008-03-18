from window import Window
import ipython_view


class Debugger(Window):

    def __init__(self, parent, main):
        Window.__init__(self, 'debugger.glade')
        self._create_text_view(main)

        #self.buffer = self.view.textview.get_buffer()
        #boxes = main.canvas.boxes
        #models = [box.model for box in boxes]
        #self.view.textview.set_editable(False)
        #self.write("canvas.boxes:\n\t" + boxes.__str__())

        #for model in models:
        #    self.write("\n\n")
        #    self.write(model.__repr__() + "\n\t")
        #    self.write(model.inspect())

    def _create_text_view(self, canvas):
        self.view.textview = ipython_view.IPythonView(canvas)
        self.view.scroll.add(self.view.textview)
        self.view.textview.show()

    def run(self):
        self.view.debugger.run()
        self.view.debugger.hide()

    #def write(self, text):
    #    #end_iter = self.buffer.get_end_iter()
    #    #self.buffer.insert(end_iter, text)
