import dialogs.leave
import time

dialog = dialogs.leave.Leave("Ejemplo.pybox", 5, time.time(), None)
response = dialog.run()
print "Response are:", response
