import gtk
import goocanvas

window = gtk.Window()
canvas = goocanvas.Canvas()
root = canvas.get_root_item()

message1 = goocanvas.Text(text="default font")
root.add_child(message1)

message2 = goocanvas.Text(text="arial font", font="Arial 10")
message2.translate(0, 50)
root.add_child(message2)

window.add(canvas)

window.connect("destroy", gtk.main_quit)
window.show_all()
gtk.main()
