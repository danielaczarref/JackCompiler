from JackTokenizer import JackTokenizer
import re




def printOpenningXMLNameplate(tag, ident):
    print("{}<{}>".format(ident, tag))

def printClosingXMLNameplate(tag, ident):
    print("{}</{}>".format(ident, tag))


class AnalisadorSintatico:

    def __init__(self, input_file):
        self.tokenizer = JackTokenizer(input_file)

    def compile(self):
        if(self.compileClass()):
            print ("Success!")
        else:
            print ("Error")

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

        while self.tokenizer.getToken() in ["var"]:  # aqui podemos ter uma declaração assim:  boolean var1, char var2, int var3;
            self.compileVarDec()


        while self.tokenizer.getToken() in ["let", "if", "while", "do", "return"]:  # aqui podemos ter uma declaração assim:  boolean var1, char var2, int var3;
            self.compileStatements()




        printClosingXMLNameplate("subroutineBody", "\t\t\t")



    def compileParameterList(self):
        self.printXMLNameplate(
            "\t\t\t")
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            return False
        self.printXMLNameplate("\t\t\t")
        self.tokenizer.advance()

        if (self.tokenizer.getToken() == ","):
            self.printXMLNameplate("\t\t\t")
            self.tokenizer.advance()

    def compileVarDec(self):
        printOpenningXMLNameplate("varDec", "\t\t\t\t")
        self.printXMLNameplate("\t\t\t\t\t")
        self.tokenizer.advance()
        if (self.tokenizer.getToken() not in ["int", "char", "boolean"]):  # className?
            return False
        self.printXMLNameplate("\t\t\t\t\t")
        self.tokenizer.advance()



        while self.tokenizer.tokenType() == self.tokenizer.IDENTIFIER:
            self.printXMLNameplate("\t\t\t\t\t")
            self.tokenizer.advance()
            if (self.tokenizer.getToken() == ","):
                self.printXMLNameplate("\t\t\t\t\t")
                self.tokenizer.advance()


        if(self.tokenizer.getToken() != ";"):
            return False

        self.printXMLNameplate("\t\t\t\t\t")
        self.tokenizer.advance()
        printClosingXMLNameplate("varDec", "\t\t\t\t")

    def compileStatements(self):

        if(self.tokenizer.getToken() == "let"):
            self.compileLet()
        elif (self.tokenizer.getToken() == "if"):
            pass
            #  self.compileIf()
        elif (self.tokenizer.getToken() == "while"):
            pass
            #self.compileWhile()
    
        elif (self.tokenizer.getToken() == "do"):
            pass
            # self.compileDo()
        elif (self.tokenizer.getToken() == "return"):
            pass
            # self.compileReturn()
        else:
            return False


    def compileLet(self): # apenas aceita esse formato -> let varName = expression ;
        printOpenningXMLNameplate("letStatement", "\t\t\t\t")
        self.printXMLNameplate("\t\t\t\t")  # print letStatement
        self.tokenizer.advance()
        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            return False
        self.printXMLNameplate("\t\t\t\t")  # print varName
        self.tokenizer.advance()



        self.printXMLNameplate("\t\t\t\t")  # print =
        self.tokenizer.advance()

        self.compileExpression()

        # Todo: compileExpression();


        if (self.tokenizer.getToken() != ";"):
            return False
        self.printXMLNameplate("\t\t\t\t")  # print =
        self.tokenizer.advance()

        printClosingXMLNameplate("letStatement", "\t\t\t\t")

    def compileWhile(self):
        return True


    def compileExpression(self):
        printOpenningXMLNameplate("expression", "\t\t\t\t")
        self.compileTerm()

        while (self.tokenizer.getToken() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]):
            self.printXMLNameplate("\t\t\t\t\t") 
            self.tokenizer.advance()
            self.compileTerm()
        if (self.tokenizer.getToken() != ";"):
            return False
        self.printXMLNameplate("\t\t\t\t")  # print =
        self.tokenizer.advance()

        printClosingXMLNameplate("expression", "\t\t\t\t")

    def compileTerm(self):
        printOpenningXMLNameplate("term", "\t\t\t\t\t")
        
        aux = False
        if (self.tokenizer.tokenType() == self.tokenizer.INTEGER_CONSTANT):
            aux = True
            self.printXMLNameplate("\t\t\t\t\t\t") 
        elif (self.tokenizer.tokenType() == self.tokenizer.STRING_CONSTANT):
            aux = True
            self.printXMLNameplate("\t\t\t\t\t\t") 
        elif (self.tokenizer.KEYWORD):
            key = self.tokenizer.KEYWORD
            print('teste key: ' + key)

            if key not in ("true", "false", "null", "this"):
                return False
            aux = True
            self.printXMLNameplate("\t\t\t\t\t\t")
        elif (self.tokenizer.getToken == "("):
            self.printXMLNameplate("\t\t\t\t\t\t")
            self.tokenizer.advance()
            self.compileExpression()

            if (self.tokenizer.getToken() != ")"):
               return False

            aux = True
            self.printXMLNameplate("\t\t\t\t\t\t")

        elif (self.tokenizer.getToken() in ["-","~"]):
            self.printXMLNameplate("\t\t\t\t\t\t")
            self.tokenizer.advance()
            self.compileTerm()
        
        elif (self.tokenizer.tokenType()== self.tokenizer.IDENTIFIER):
            self.printXMLNameplate("\t\t\t\t\t\t")
            self.tokenizer.advance()

            if (self.tokenizer.getToken() == "["):
                self.printXMLNameplate("\t\t\t\t\t\t")
                self.tokenizer.advance()
                self.compileExpression()

                if (self.tokenizer.getToken != "]"):
                    return False
                
                aux = True
                self.printXMLNameplate("\t\t\t\t\t\t")

            elif (self.tokenizer.getToken() == "("):
                self.printXMLNameplate("\t\t\t\t\t\t")
                self.tokenizer.advance()
                #self.compileExpressionList()
                #todo compile expression list

                if (self.tokenizer.getToken() != ")"):
                    return False
                
                aux = True
                self.printXMLNameplate("\t\t\t\t\t\t")

            elif (self.tokenizer.getToken() == "."):
                self.printXMLNameplate("\t\t\t\t\t\t")
                self.tokenizer.advance()

                if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                    return False

                self.printXMLNameplate("\t\t\t\t\t\t")
                self.tokenizer.advance()

                if (self.tokenizer.getToken() != "("):
                    return False
                self.printXMLNameplate("\t\t\t\t\t\t")
                self.tokenizer.advance()
                #self.compileExpressionList

                if (self.tokenizer.getToken() != ")"):
                    return False
                self.printXMLNameplate("\t\t\t\t\t\t")
                self.tokenizer.advance()
        if aux == True:
            self.tokenizer.advance()
        printOpenningXMLNameplate("term", "\t\t\t\t\t")
