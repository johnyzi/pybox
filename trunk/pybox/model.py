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
        print "Name : ", self.name

        if self.abstract:
            print "Is abstract : YES"
        else:
            print "Is abstract : NO"

        print "Superclass : ", self.superclass
        print "Comments : ", self.comment
        print "Attributes : ", self.variables
        print "Methods : ", self.methods


if __name__ == '__main__':
   
    new = ClassModel("persona", "", True, "", [], [])
    new.show()
