from JackTokenizer.JackTokenizer import JackTokenizer




def printOpenningXMLNameplate(tag):
    print("</{}>".format(tag))

def printClosingXMLNameplate(tag):
    print("</{}>".format(tag))


class Engine:

    def __init__(self, input_file, output):
        self.tokenizer = JackTokenizer(input_file)
        self.output_file = open(output, "w")

        if(self.compileClass()):
            print("Success")
        else:
            print("Error")
        self.output_file.close()

    def printXMLNameplate(self, ident):
        print("{}<{}> {} </{}>".format(ident,self.tokenizer.tokenType(), self.tokenizer.getToken(), self.tokenizer.tokenType()))


    def compileClass(self):
        printOpenningXMLNameplate("class")

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

        # Todo() compileClassCarDec()

        # Esperando uma ou varias subroutineDec

        # Todo(): compileSubroutineDec()


        if (self.tokenizer.getToken() != "}"):
            return False
        self.printXMLNameplate("\t")


        printClosingXMLNameplate("class")


        return True  # Tudo ok, é uma classe
