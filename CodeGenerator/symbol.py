
class SymbolTable():

    def __init__(self):

        self.table = {}

        self.subroutineTable = {}
        self.fieldTable = {}
        self.staticTable = {}


        self.static_counter = 0
        self.arg_counter = 0
        self.field_counter = 0
        self.var_counter = 0

    def addElement(self, name, _type, kind):

        if(kind == "ARG"):
            counter = self.arg_counter
            self.subroutineTable[name] = [_type, kind, counter]
            self.arg_counter += 1

        elif (kind == "VAR"):
            counter = self.var_counter
            self.subroutineTable[name] = [_type, kind, counter]
            self.var_counter += 1


        elif (kind == "STATIC"):
            counter = self.static_counter
            self.staticTable[name] = [_type, kind, counter]
            self.static_counter += 1

        else:
            counter = self.field_counter
            self.fieldTable[name] = [_type, kind, counter]
            self.field_counter += 1


    def clear(self):
        self.subroutineTable.clear()
        self.arg_counter = 0
        self.var_counter = 0

    def returnIdentifier(self, key):
        if(key in self.staticTable):
            return self.staticTable[key]

        elif(key in self.fieldTable):
            return self.fieldTable[key]

        elif(key in self.subroutineTable):
            return self.subroutineTable[key]

        else:
            return False

    def printTable(self):
        print("Imprimindo tabela {}".format(self.reference))
        for i in self.table.keys():
            print(self.table[i])
