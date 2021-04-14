

class CodeWriter:

    def __init__(self, file):
        self.file = file
        self.output = open(file.split(".")[0]+".out", "w")

        self.helperDict = {
            "POINTER" : "pointer",
            "LOCAL"   : "local",
            "THAT"    : "that",
            "THIS"    : "this",
            "TEMP"    : "temp",
            "STATIC"  : "static"
        }

    def pop(self, segmento, indice):

        foo = self.helperDict.get(segmento)

        if(foo == None):
            print("Code Writer - Erro 1")
            return False

        print("pop {} {}".format(segmento, indice), file=self.output)

    def push (self, segmento, indice):

        foo = self.helperDict.get(segmento)

        if(foo == None):
            print("Code Writer - Erro 1.1")

            return False

        print("push {} {}".format(segmento, indice), file=self.output)


    def writeReturn(self):
        print("return", file=self.output)

    def writeGoto(self, label):
        print("goto  {}".format(label), file=self.output)

    def writeIfGoto(self, label):
        print("if-goto {}".format(label), file=self.output)

    def writeLabel(self, label):
        print("label {}".format(label), file=self.output)

    def writeCall(self, name, len_args):
        print("call {} {}".format(name, len_args), file=self.output)

    def writeFunction(self, name, len_local):
        print("call {} {}".format(name, len_local), file=self.output)

    def writeExpression(self, command):

        if command not in ["ADD", "SUB", "NEG", "EQ", "GT", "LT", "AND", "OR", "NOT"]:
            print("Code Writer - Erro 2")
            return False
        lowerCase = command.lower()
        print(command, file=self.output)

        pass

    def close(self):
        self.output.close()
