class Model:

    def __init__(self, name="Persona", superclass="", abstract=False, comment="",
            variables=['a1', 'a2'], methods=['m1', 'm2']):
        self.name = name
        self.superclass = superclass
        self.abstract = abstract
        self.comment = comment
        self.variables = variables
        self.methods = methods

    def show(self):
        print "Name : ", self.name

        if self.abstract:
            print "Is abstract : YES"
        else:
            print "Is abstract : NO"

        print "Comments : ", self.comment
        print "Attributes : ", self.variables
        print "Methods : ", self.methods


if __name__ == '__main__':
   
    new = ClassModel("persona", "", True, "", [], [])
    new.show()
