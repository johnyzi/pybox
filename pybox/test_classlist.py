# -*- encoding: utf-8 -*
import gtk
import dialogs

if __name__ == '__main__':
    dialog = dialogs.classlist.ClassList(['Pet', 'Person'], ['Pet'])
    response = dialog.run()
    print "Selected classes are:", response
