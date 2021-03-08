from JackTokenizer.JackTokenizer import JackTokenizer




def printOpenningXMLNameplate(tag, ident):
    print("{}<{}>".format(ident, tag))

def printClosingXMLNameplate(tag, ident):
    print("{}</{}>".format(ident, tag))


class AnalisadorSintatico:

    def __init__(self, input_file, output):
        self.tokenizer = JackTokenizer(input_file)
        self.output_file = open(output, "w")

        if(self.compileClass()):
            print("Success")
        else:
            print("Error")
        self.output_file.close()

    def printXMLNameplate(self, ident):
        print("{}<{}> {} </{}>".format(ident, self.tokenizer.tokenType(), self.tokenizer.getToken(), self.tokenizer.tokenType()))


    def compileClass(self):
        printOpenningXMLNameplate("class", "")

        if(self.tokenizer.getToken() != "class"):
            return False  # não é uma classe pois esperavamos a keyword "classe" aqui

        self.printXMLNameplate("\t")

        self.tokenizer.advance()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            return False  # não é uma classe pois esperavamos um identificador aqui

        self.printXMLNameplate("\t")

        self.tokenizer.advance()

        if (self.tokenizer.getToken() != "{"):
            return False
        self.printXMLNameplate("\t")

        self.tokenizer.advance()

        # Esperando uma ou varias classVarDec
        while (self.tokenizer.getToken() == "static" or self.tokenizer.getToken() == "field"):
            self.compileClassVarDec()


        # Esperando uma ou varias subroutineDec
        while (self.tokenizer.getToken() in ["constructor", "function", "method"]):
            self.compileSubroutineDec()


        if (self.tokenizer.getToken() != "}"):
            return False
        self.printXMLNameplate("\t")


        printClosingXMLNameplate("class", "")


        return True  # Tudo ok, é uma classe

    def compileClassVarDec(self):
        printOpenningXMLNameplate("classVarDec", "\t\t")

        self.printXMLNameplate("\t\t\t")  # esperamos static ou field

        self.tokenizer.advance()

        # devo identificar que tipo de identificador (int | char | boolean | className)? O tipo aqui ta indo como uma keyword
        if(self.tokenizer.getToken() not in ["int", "char", "boolean"]):  # Todo(): nao considerei que o tipo pode ser className.
            return False

        self.printXMLNameplate("\t\t\t")

        self.tokenizer.advance()

        if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            return False

        while self.tokenizer.tokenType() == self.tokenizer.IDENTIFIER:  # aqui podemos ter uma declaração assim: static boolean var1,var2,var3;
            self.printXMLNameplate("\t\t\t")
            self.tokenizer.advance()

            if(self.tokenizer.getToken() == ","):
                self.printXMLNameplate("\t\t\t")
                self.tokenizer.advance()


        if(self.tokenizer.getToken() != ";"):
            return False

        self.printXMLNameplate("\t\t\t")  # imprime o ;


        self.tokenizer.advance()   # avanca e passa o controle de volta ao metodo compileClass
        printClosingXMLNameplate("classVarDec", "\t\t")

    def compileSubroutineDec(self):
        printOpenningXMLNameplate("subroutineDec", "\t\t")

        self.printXMLNameplate("\t\t\t")
        self.tokenizer.advance()

        # esperamos o tipo : void ou type
        if(self.tokenizer.getToken() not in ["void", "int", "char", "boolean"]): # className?
            return False

        self.printXMLNameplate("\t\t\t")
        self.tokenizer.advance()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            return False

        self.printXMLNameplate("\t\t\t")

        self.tokenizer.advance()

        if(self.tokenizer.getToken() != "("):
            return False
        self.printXMLNameplate("\t\t\t")

        self.tokenizer.advance()

        # if(self.tokenizer.getToken() not in ["void", "int", "char", "boolean"]):
        #     return False  # esperamos um type aqui
        #
        # self.printXMLNameplate("\t\t\t")
        # self.tokenizer.advance()



        while self.tokenizer.getToken() in ["int", "char", "boolean"]:  # aqui podemos ter uma declaração assim:  boolean var1, char var2, int var3;
            self.compileParameterList()


        if(self.tokenizer.getToken() != ")"):
            return False

        self.printXMLNameplate("\t\t\t")
        self.tokenizer.advance()

        if(self.tokenizer.getToken() != "{"):
            return False

        self.printXMLNameplate("\t\t\t")
        self.tokenizer.advance()

        printOpenningXMLNameplate("subroutineBody", "\t\t\t")

        # Todo(): compileVarDec*()
        printOpenningXMLNameplate("varDec", "\t\t\t\t")
        printClosingXMLNameplate("varDec", "\t\t\t\t")
        printOpenningXMLNameplate("varDec", "\t\t\t\t")
        printClosingXMLNameplate("varDec", "\t\t\t\t")

        # Todo(): compileStatement*()
        printOpenningXMLNameplate("Xstatement", "\t\t\t\t")
        printClosingXMLNameplate("Ystatement", "\t\t\t\t")

        printClosingXMLNameplate("subroutineBody", "\t\t\t")


        printClosingXMLNameplate("subroutineDec", "\t\t")

    def compileParameterList(self):
        self.printXMLNameplate(
            "\t\t\t")  # TODO(): o corpo desse while deve ser encapsulado no metodo compileParameterList
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            return False
        self.printXMLNameplate("\t\t\t")
        self.tokenizer.advance()

        if (self.tokenizer.getToken() == ","):
            self.printXMLNameplate("\t\t\t")
            self.tokenizer.advance()



