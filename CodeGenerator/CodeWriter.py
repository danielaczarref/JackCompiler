

class CodeWriter:

    def __init__(self, file):
        self.file = file
        self.output = open(file.split(".")[0]+".vm", "w")

        self.helperDict = {
            "POINTER" : "pointer",
            "LOCAL"   : "local",
            "THAT"    : "that",
            "THIS"    : "this",
            "TEMP"    : "temp",
            "STATIC"  : "static",
            "ARG" : "argument",
            "CONST": "constant",
            "FIELD" : "this"
        }

    def pop(self, segmento, indice):

        replaced = self.helperDict.get(segmento)

        if(replaced == None):
            print("Code Writer - Erro 1")
            raise Exception
        # self.output.append("pop {} {}".format(replaced, indice))
        print("pop {} {}".format(replaced, indice), file=self.output)

    def push (self, segmento, indice):

        replaced = self.helperDict.get(segmento)

        if(replaced == None):
            print("Code Writer - Erro 2")

            return Exception

        # self.output.append("push {} {}".format(replaced, indice))
        #
        print("push {} {}".format(replaced, indice), file=self.output)


    def writeReturn(self):
        # self.output.append("return")
        print("return", file=self.output)

    def writeGoto(self, label):
        # self.output.append("goto {}".format(label))
        print("goto {}".format(label), file=self.output)

    def writeIfGoto(self, label):
        # self.output.append("if-goto {}".format(label))
        print("if-goto {}".format(label), file=self.output)

    def writeLabel(self, label):
        # self.output.append("label {}".format(label))
        print("label {}".format(label), file=self.output)

    def writeCall(self, name, len_args):
        # self.output.append("call {} {}".format(name, len_args))
        print("call {} {}".format(name, len_args), file=self.output)

    def writeFunction(self, name, len_local):
        # self.output.append("function {} {}".format(name, len_local))
        print("function {} {}".format(name, len_local), file=self.output)

    def writeExpression(self, command):

        if command not in ["ADD", "SUB", "NEG", "EQ", "GT", "LT", "AND", "OR", "NOT"]:
            print("Code Writer - Erro 2")
            raise Exception
        lowerCase = command.lower()
        # self.output.append(lowerCase)

        print(lowerCase, file=self.output)


    def close(self):
        # for i in self.output:
        #     print(i)
        self.output.close()
