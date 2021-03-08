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
        # Todo(): compileSubroutineDec()


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
        if(self.tokenizer.getToken() not in ["int", "char", "boolean"]):  # nao considerei que o tipo pode ser className.
            return False

        self.printXMLNameplate("\t\t\t")

        self.tokenizer.advance()

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


