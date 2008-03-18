class Model:

    def __init__(self, name="", superclass=[], abstract=False, comment="",
            variables=[], methods=[]):
        self.name = name
        self.superclass = superclass
        self.abstract = abstract
        self.comment = comment
        self.variables = variables
        self.methods = methods

    def __repr__(self):
        return "<Model instance named='%s'>" %(self.name)

    def inspect(self):
        values = [
                ('name', self.name),
                ('superclass', self.superclass),
                ('abstract', self.abstract),
                ('attributes', self.variables),
                ('methods', self.methods),
                ]

        print '\t', self
        for key, value in values:
            print "\t\t%s: %s" %(key, repr(value))

if __name__ == '__main__':
    new = Model("Person", [], True, "", [], [])
    print new.inspect()
