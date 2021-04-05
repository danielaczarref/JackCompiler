

class SymbolTable:

    def __init__(self, ref):
        self.reference = ref
        self.table = {}


    def addIdentifier(self, name, type_, kind, value):

        self.table[name] = {"name":  name, "type": type_, "kind": kind, "#": value}

    def printTable(self):
        print("Imprimindo tabela {}".format(self.reference))
        for i in self.table.keys():
            print(self.table[i])
