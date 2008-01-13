    # -*- encoding: utf-8 -*
import gtk
import dialogs
import model

if __name__ == '__main__':
    model = model.Model("animales", "caca", True, '', ['var1', 'var2', 'var3'])
    new = dialogs.classview.ClassView(model)
    print new.view.dialog1.run()

