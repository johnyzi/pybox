import dialogs.leave
import time

dialog = dialogs.leave.Leave("Ejemplo.pybox", 5, time.time())
print dialog.run()
