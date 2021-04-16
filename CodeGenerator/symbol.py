
class SymbolTable(dict):

    def __init__(self, *args):

        dict.__init__(self, *args)

        self.subroutineTable = {}
        self.staticTable = {}

        self.fieldTable = {}

        self._count = {
            'STATIC': 0,
            'ARG': 0,
            'FIELD': 0,
            'VAR': 0
        }

    def getCount(self, kind):
        return self._count[kind]

    def addElement(self, name, _type, kind):


        try:
            i = self._count[kind]
        except KeyError:
            raise Exception

        if(kind in ["ARG", "VAR"]):
            self.subroutineTable[name] = [_type, kind, i]

        elif (kind == "STATIC"):

            self.staticTable[name] = [_type, kind, i]

        else:
            self.fieldTable[name] = [_type, kind, i]

        self._count[kind] += 1

        return i

    def clear(self):
        self.subroutineTable.clear()
        self._count["ARG"] = 0
        self._count["VAR"] = 0

    def __getitem__(self, key):
        if(key in self.staticTable):
            return self.staticTable[key]

        elif(key in self.subroutineTable):
            return self.subroutineTable[key]

        elif(key in self.fieldTable):
            return self.fieldTable[key]
        else:
            raise KeyError("{} not in any scope.")


    def get(self, key, default = (None, None, -1)):

        try:
            ret = self[key]
        except KeyError:
            ret = default
        finally:
            return ret

