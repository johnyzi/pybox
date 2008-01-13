class Model:

    def __init__(self, name="", superclass="", abstract=False, comment="",
            variables=[], methods=[]):
        self.name = name
        self.superclass = superclass
        self.abstract = abstract
        self.comment = comment
        self.variables = variables
        self.methods = methods

    def show(self):
        print "Nombre:", self.name
        if self.abstract:
            print "Is abstract: si"
        else:
            print "Is abstract: no"
        print "comment:", self.comment
        print "variables:", self.variables
        print "methods:", self.methods


if __name__ == '__main__':
   
    new = ClassModel("persona", "", True, "", [], [])
    new.show()
