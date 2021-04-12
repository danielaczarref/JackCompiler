from JackTokenizer.JackTokenizer import JackTokenizer
from CodeGenerator.symbol import SymbolTable
import re




class AnalisadorSintatico:

    def __init__(self, input_file):
        self.input_file = input_file
        self.tokenizer = JackTokenizer(input_file)
        self.output = open(input_file.split(".")[0]+".out", "a")
        self.errorMSG = None
        self.symbolTable = SymbolTable()
        self.className = None



    def compile(self):
        if(self.compileClass()):
            print("Success: {} compiled".format(self.input_file))
            self.output.close()
        else:
            print("Error while compiling file: {}".format(self.input_file) + "\n Error: "+ self.errorMSG)
            self.output.close()


    def printXMLNameplate(self):
        pass

        # print("{}<{}> {} </{}>".format("", self.tokenizer.tokenType(), self.tokenizer.getToken(), self.tokenizer.tokenType()), file=self.output)

    def printOpenningXMLNameplate(self, tag):
        pass

        # print("{}<{}>".format("", tag), file=self.output)

    def printClosingXMLNameplate(self, tag):
        pass
        # print("{}</{}>".format("", tag), file=self.output)


    def compileClass(self):
        self.printOpenningXMLNameplate("class")

        # if(self.tokenizer.getToken() != "class"):
        #     self.errorMSG = "Method compileClass(). Expected keyword class but {} was given".format(self.tokenizer.getToken())
        #     return False  # não é uma classe pois esperavamos a keyword "classe" aqui

        self.printXMLNameplate()
        self.tokenizer.advance() # class

        self.className = self.tokenizer.getToken()

        self.printXMLNameplate()
        self.tokenizer.advance() # className

        self.printXMLNameplate()
        self.tokenizer.advance()  # {

        while (self.tokenizer.getToken() in ["static", "field"]):
            self.compileClassVarDec()

        while (self.tokenizer.getToken() in ["method", "constructor", "function"]):
            self.compileSubroutineDec()


        self.printXMLNameplate()
        self.tokenizer.advance() # }

        self.printClosingXMLNameplate("class")
        self.symbolTable.printStaticTable("Static Table")
        # self.symbolTable.printFieldTable("Field Table")

        return True  # Tudo ok, é uma classe


    def compileClassVarDec(self):
        self.printOpenningXMLNameplate("classVarDec")


        kind = self.tokenizer.getToken().upper()

        self.printXMLNameplate()
        self.tokenizer.advance() # static ou field

        tipo = self.tokenizer.getToken()

        self.printXMLNameplate()
        self.tokenizer.advance() # type

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            return False

        self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)

        self.printXMLNameplate()
        self.tokenizer.advance()  # type


        while self.tokenizer.getToken() != ';':
            self.printXMLNameplate()
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                return False
            self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
            self.printXMLNameplate()
            self.tokenizer.advance()

        self.printXMLNameplate()
        self.tokenizer.advance()
        self.printClosingXMLNameplate("classVarDec")



        return True

    def compileSubroutineDec(self):
        self.printOpenningXMLNameplate("subroutineDec")

        self.symbolTable.clear()

        tipo = self.tokenizer.getToken()

        if(tipo == "method"):
            self.symbolTable.addElement("this", self.className, "ARG")

        self.printXMLNameplate()
        self.tokenizer.advance() # method, constructor, function


        self.printXMLNameplate()
        self.tokenizer.advance()  # type

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            return False

        class_name = self.tokenizer.getToken()

        self.printXMLNameplate()
        self.tokenizer.advance()  # identifier

        self.printXMLNameplate()
        self.tokenizer.advance()  # (

        self.compileParameterList()

        self.printXMLNameplate()
        self.tokenizer.advance()  # )

        self.printXMLNameplate()
        self.tokenizer.advance()  # {

        while self.tokenizer.getToken() == "var":
            self.compileVarDec()


        self.compileStatements()

        self.printXMLNameplate()
        self.tokenizer.advance()  # }


        self.symbolTable.printSubroutineTable("Subroutine {}".format(class_name))

        self.printClosingXMLNameplate("subroutineDec")
        return True

    def compileParameterList(self):
        self.printOpenningXMLNameplate("parameterList")

        kind = "ARG"

        if(self.tokenizer.getToken() == ")"):
            self.printClosingXMLNameplate("parameterList")
            return True

        tipo = self.tokenizer.getToken()
        self.printXMLNameplate()
        self.tokenizer.advance()  # type

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            return False

        self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)

        self.printXMLNameplate()
        self.tokenizer.advance()  # identifier

        while self.tokenizer.getToken() != ")":
            self.printXMLNameplate()
            self.tokenizer.advance()  # ,

            tipo = self.tokenizer.getToken()

            self.printXMLNameplate()
            self.tokenizer.advance()  #

            if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                return False
            self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
            self.printXMLNameplate()
            self.tokenizer.advance()  #
        self.printClosingXMLNameplate("parameterList")

        return True


    def compileVarDec(self):

        self.printOpenningXMLNameplate("varDec")

        self.printXMLNameplate()
        self.tokenizer.advance()  #var

        kind = "VAR"
        tipo = self.tokenizer.getToken()

        self.printXMLNameplate()
        self.tokenizer.advance()  # type

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            return False
        self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
        self.printXMLNameplate()
        self.tokenizer.advance()  # identifier

        while self.tokenizer.getToken() != ";":
            self.printXMLNameplate()
            self.tokenizer.advance()  # t,
            if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                return False
            self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
            self.printXMLNameplate()
            self.tokenizer.advance()  #

        self.printXMLNameplate()
        self.tokenizer.advance()  #
        self.printClosingXMLNameplate("varDec")




    def compileStatements(self):
        self.printOpenningXMLNameplate("compileStatements")

        while self.tokenizer.getToken() in ["return", "let", "do", "if", "while"]:
            if(self.tokenizer.getToken() == "if"):
                self.compileIf()
            elif (self.tokenizer.getToken() == "while"):
                self.compileWhile()
            elif (self.tokenizer.getToken() == "let"):
                self.compileLet()
            elif (self.tokenizer.getToken() == "do"):
                self.compileDo()
            elif (self.tokenizer.getToken() == "return"):
                self.compileReturn()
        self.printClosingXMLNameplate("compileStatements")

    def compileIf(self):
        self.printOpenningXMLNameplate("ifStatement")

        self.printXMLNameplate()
        self.tokenizer.advance()  # if

        self.printXMLNameplate()
        self.tokenizer.advance()  # (

        self.compileExpression()

        self.printXMLNameplate()
        self.tokenizer.advance()  # )

        self.printXMLNameplate()
        self.tokenizer.advance()  # {

        self.compileStatements()

        self.printXMLNameplate()
        self.tokenizer.advance()  # }


        self.printClosingXMLNameplate("ifStatement")
        return True

    def compileWhile(self):
        self.printOpenningXMLNameplate("whileStatement")

        self.printXMLNameplate()
        self.tokenizer.advance()  # while

        self.printXMLNameplate()
        self.tokenizer.advance()  # (

        self.compileExpression()

        self.printXMLNameplate()
        self.tokenizer.advance()  # )

        self.printXMLNameplate()
        self.tokenizer.advance()  # {

        self.compileStatements()

        self.printXMLNameplate()
        self.tokenizer.advance()  # }
        self.printClosingXMLNameplate("whileStatement")


        return True

    def compileLet(self):
        self.printOpenningXMLNameplate("letStatement")

        self.printXMLNameplate()
        self.tokenizer.advance()  # let

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            return False

        self.printXMLNameplate()
        self.tokenizer.advance()  # identifier

        if(self.tokenizer.getToken() == "["):
            self.printXMLNameplate()
            self.tokenizer.advance() # [

            self.compileExpression()

            self.printXMLNameplate()
            self.tokenizer.advance()  # ]

            self.printXMLNameplate()
            self.tokenizer.advance()  # =

            self.compileExpression()
        else:

            self.printXMLNameplate()
            self.tokenizer.advance()  # =

            self.compileExpression()

        self.printXMLNameplate()
        self.tokenizer.advance()  # ;
        self.printClosingXMLNameplate("letStatement")
        return True

    def compileReturn(self):
        self.printOpenningXMLNameplate("returnStatement")

        self.printXMLNameplate()
        self.tokenizer.advance()  # return

        if(self.tokenizer.getToken() != ";"):
            self.compileExpression()

        self.printXMLNameplate()
        self.tokenizer.advance()  # ;



        self.printClosingXMLNameplate("returnStatement")
        return True

    def compileDo(self):
        self.printOpenningXMLNameplate("compileDo")

        self.printXMLNameplate()
        self.tokenizer.advance()  # do

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            return False

        self.printXMLNameplate()
        self.tokenizer.advance()  # identifier

        self.compileSubroutineCall()

        self.printXMLNameplate()
        self.tokenizer.advance()  # ;

        self.printClosingXMLNameplate("compileDo")

        return True

    def compileExpression(self):
        self.printOpenningXMLNameplate("compileExpression")

        self.compileTerm()

        while (self.tokenizer.getToken() in self.tokenizer.operatorArray):
            self.printXMLNameplate()
            self.tokenizer.advance()  # ,

            self.compileTerm()

        self.printClosingXMLNameplate("compileExpression")
        return True

    def compileExpressionList(self):
        self.printOpenningXMLNameplate("compileExpressionList")

        len_args = 0

        if(self.tokenizer.getToken() == ")"):
            return len_args

        self.compileExpression()
        len_args = len_args + 1

        while (self.tokenizer.getToken() != ")"):

            self.printXMLNameplate()
            self.tokenizer.advance()  # ,
            self.compileExpression()
            len_args = len_args + 1

        self.printClosingXMLNameplate("compileExpressionList")

        return len_args

    def compileSubroutineCall(self):
        self.printOpenningXMLNameplate("compileSubroutineCall")

        if(self.tokenizer.getToken() == "."):
            self.printXMLNameplate()
            self.tokenizer.advance()  # .

            self.printXMLNameplate()
            self.tokenizer.advance()  # identifier

        self.printXMLNameplate()
        self.tokenizer.advance()  # (

        self.compileExpressionList()

        self.printXMLNameplate()
        self.tokenizer.advance()  # )

        self.printClosingXMLNameplate("compileSubroutineCall")

        return True

    def compileString(self):
        self.printXMLNameplate()
        self.tokenizer.advance()  # string

    def compileTerm(self):
        self.printOpenningXMLNameplate("compileTerm")

        if(self.tokenizer.tokenType() == self.tokenizer.STRING_CONSTANT):
            self.compileString()
        elif(self.tokenizer.tokenType() == self.tokenizer.INTEGER_CONSTANT):
            self.printXMLNameplate()
            self.tokenizer.advance()  # int

        elif(self.tokenizer.getToken() in ["false", "null", "true"]):
            self.printXMLNameplate()
            self.tokenizer.advance()  # keyword

        elif(self.tokenizer.getToken() == "this"):
            self.printXMLNameplate()
            self.tokenizer.advance()  # this

        elif(self.tokenizer.getToken() in ["-", "~"]):
            self.printXMLNameplate()
            self.tokenizer.advance()  #

            self.compileTerm()
        elif(self.tokenizer.getToken() == "("):

            self.printXMLNameplate()
            self.tokenizer.advance()  # (

            self.compileExpression()
            self.printXMLNameplate()

            self.tokenizer.advance()  # )
        else:
            if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                return False

            self.printXMLNameplate()
            self.tokenizer.advance()  # identifier

            if(self.tokenizer.getToken() == "["):
                self.printXMLNameplate()
                self.tokenizer.advance()  # [
                self.compileExpression()
                self.printXMLNameplate()
                self.tokenizer.advance()  # ]

            elif(self.tokenizer.getToken() in [".", "("]):
                self.compileSubroutineCall()



        self.printClosingXMLNameplate("compileTerm")

        return True
