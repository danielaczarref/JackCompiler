from JackTokenizer.JackTokenizer import JackTokenizer
import re




class AnalisadorSintatico:

    def __init__(self, input_file):
        self.input_file = input_file
        self.tokenizer = JackTokenizer(input_file)
        self.output = open(input_file.split(".")[0]+".cjack", "a")
        self.errorMSG = None

    def compile(self):
        if(self.compileClass()):
            print("Success: {} compiled".format(self.input_file))
            self.output.close()
        else:
            print("Error while compiling file: {}".format(self.input_file) + "\n Error: "+ self.errorMSG)
            self.output.close()


    def printXMLNameplate(self, ident):
        print("{}<{}> {} </{}>".format("", self.tokenizer.tokenType(), self.tokenizer.getToken(), self.tokenizer.tokenType()), file=self.output)

    def printOpenningXMLNameplate(self, tag, ident):
        print("{}<{}>".format("", tag), file=self.output)

    def printClosingXMLNameplate(self, tag, ident):
        print("{}</{}>".format("", tag), file=self.output)


    def compileClass(self):
        self.printOpenningXMLNameplate("class", "")

        if(self.tokenizer.getToken() != "class"):
            self.errorMSG = "Method compileClass(). Expected keyword class but {} was given".format(self.tokenizer.getToken())
            return False  # não é uma classe pois esperavamos a keyword "classe" aqui

        self.printXMLNameplate("\t")

        self.tokenizer.advance()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            self.errorMSG = "Method compileClass(). Expected identifier but {} was given".format(self.tokenizer.tokenType())
            return False  # não é uma classe pois esperavamos um identificador aqui

        self.printXMLNameplate("\t")

        self.tokenizer.advance()

        if (self.tokenizer.getToken() != "{"):
            self.errorMSG = 'Method compileClass(). Expected symbol "{{" but {} was given'.format(self.tokenizer.getToken())

            return False
        self.printXMLNameplate("\t")

        self.tokenizer.advance()

        # Esperando uma ou varias classVarDec
        while (self.tokenizer.getToken() == "static" or self.tokenizer.getToken() == "field"):
            self.compileClassVarDec()


        # Esperando uma ou varias subroutineDec
        while (self.tokenizer.getToken() in ["constructor", "function", "method"]):
            self.compileSubroutineDec()

        # self.tokenizer.advance()

        if (self.tokenizer.getToken() != "}"):
            self.errorMSG = 'Method compileClass(). Expected symbol "}}" but {} was given'.format(self.tokenizer.getToken())

            return False
        self.printXMLNameplate("\t")



        self.printClosingXMLNameplate("class", "")


        return True  # Tudo ok, é uma classe

    def compileClassVarDec(self):
        self.printOpenningXMLNameplate("classVarDec", "\t\t")

        self.printXMLNameplate("\t\t\t")  # esperamos static ou field

        self.tokenizer.advance()

        # devo identificar que tipo de identificador (int | char | boolean | className)? O tipo aqui ta indo como uma keyword
        if(self.tokenizer.getToken() not in ["int", "char", "boolean"]):  # Todo(): nao considerei que o tipo pode ser className.
            self.errorMSG = "Method compileClassVarDec(). Expected type (int,char,boolean) but {} was given".format(self.tokenizer.getToken())

            return False

        self.printXMLNameplate("\t\t\t")

        self.tokenizer.advance()

        if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            self.errorMSG = "Method compileClassVarDec(). Expected identifier but {} was given".format(self.tokenizer.tokenType())
            return False

        while self.tokenizer.tokenType() == self.tokenizer.IDENTIFIER:  # aqui podemos ter uma declaração assim: static boolean var1,var2,var3;
            self.printXMLNameplate("\t\t\t")
            self.tokenizer.advance()

            if(self.tokenizer.getToken() == ","):
                self.printXMLNameplate("\t\t\t")
                self.tokenizer.advance()


        if(self.tokenizer.getToken() != ";"):
            self.errorMSG = "Method compileClassVarDec(). Expected symbol ';' but {} was given".format(self.tokenizer.getToken())

            return False

        self.printXMLNameplate("\t\t\t")  # imprime o ;


        self.tokenizer.advance()   # avanca e passa o controle de volta ao metodo compileClass
        self.printClosingXMLNameplate("classVarDec", "\t\t")

    def compileSubroutineDec(self):
        self.printOpenningXMLNameplate("subroutineDec", "\t\t")

        self.printXMLNameplate("\t\t\t")
        self.tokenizer.advance()

        # esperamos o tipo : void ou type
        if(self.tokenizer.getToken() not in ["void", "int", "char", "boolean"]): # className?
            self.errorMSG = "Method compileSubRoutineDec(). Expected keyword for type (void, int, char, boolean) but {} was given".format(self.tokenizer.getToken())
            return False

        self.printXMLNameplate("\t\t\t")
        self.tokenizer.advance()

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            self.errorMSG = "Method compileSubRoutineDec(). Expected identifier but {} was given".format(self.tokenizer.tokenType())

            return False

        self.printXMLNameplate("\t\t\t")

        self.tokenizer.advance()

        if(self.tokenizer.getToken() != "("):
            self.errorMSG = "Method compileSubRoutineDec(). Expected symbol '(' but {} was given".format(self.tokenizer.getToken())

            return False
        self.printXMLNameplate("\t\t\t")

        self.tokenizer.advance()

        # if(self.tokenizer.getToken() not in ["void", "int", "char", "boolean"]):
        #     return False  # esperamos um type aqui
        #
        # self.printXMLNameplate("\t\t\t")
        # self.tokenizer.advance()



        while self.tokenizer.getToken() in ["int", "char", "boolean"]:  # aqui podemos ter uma declaração assim:  boolean var1, char var2, int var3;
            self.errorMSG = "Method compileSubRoutineDec(). Expected type (int, char, boolean) but {} was given".format(self.tokenizer.getToken())

            self.compileParameterList()


        if(self.tokenizer.getToken() != ")"):
            self.errorMSG = "Method compileSubRoutineDec(). Expected symbol ')' but {} was given".format(self.tokenizer.getToken())

            return False

        self.printXMLNameplate("\t\t\t")
        self.tokenizer.advance()

        if(self.tokenizer.getToken() != "{"):
            self.errorMSG = "Method compileSubRoutineDec(). Expected symbol '{{' but {} was given".format(self.tokenizer.getToken())

            return False

        self.printXMLNameplate("\t\t\t")
        self.tokenizer.advance()

        self.printOpenningXMLNameplate("subroutineBody", "\t\t\t")

        while self.tokenizer.getToken() in ["var"]:  # aqui podemos ter uma declaração assim:  boolean var1, char var2, int var3;
            self.errorMSG = "Method compileSubRoutineDec(). Expected keyword 'var' but {} was given".format(self.tokenizer.getToken())

            self.compileVarDec()


        while self.tokenizer.getToken() in ["let", "if", "while", "do", "return"]:  # aqui podemos ter uma declaração assim:  boolean var1, char var2, int var3;
            self.compileStatements()

        self.printXMLNameplate("\t\t\t")
        
        self.printClosingXMLNameplate("subroutineBody", "\t\t\t")
        self.tokenizer.advance()



    def compileParameterList(self):
        self.printXMLNameplate(
            "\t\t\t")
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            self.errorMSG = "Method compileParameterList(). Expected identifier but {} was given".format(self.tokenizer.getToken())
            return False
        self.printXMLNameplate("\t\t\t")
        self.tokenizer.advance()

        if (self.tokenizer.getToken() == ","):
            self.printXMLNameplate("\t\t\t")
            self.tokenizer.advance()

    def compileVarDec(self):
        self.printOpenningXMLNameplate("varDec", "\t\t\t\t")
        self.printXMLNameplate("\t\t\t\t\t")
        self.tokenizer.advance()
        if (self.tokenizer.getToken() not in ["int", "char", "boolean"]):  # className?
            self.errorMSG = "Method compileVarDec(). Expected type(int,char,boolean) but {} was given".format(self.tokenizer.getToken())

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
            self.errorMSG = "Method compileVarDec(). Expected symbol ';' but {} was given".format(self.tokenizer.getToken())

            return False

        self.printXMLNameplate("\t\t\t\t\t")
        self.tokenizer.advance()
        self.printClosingXMLNameplate("varDec", "\t\t\t\t")

    def compileStatements(self):

        if(self.tokenizer.getToken() == "let"):
            self.compileLet()
        elif (self.tokenizer.getToken() == "if"):
            self.compileIf()
        elif (self.tokenizer.getToken() == "while"):
            self.compileWhile()
    
        elif (self.tokenizer.getToken() == "do"):
            pass
            #self.compileDo()
        elif (self.tokenizer.getToken() == "return"):
            self.compileReturn()
        else:
            self.errorMSG = "Method compileStatements(). Expected statement (let, if, while, do, return) but {} was given".format(self.tokenizer.getToken())

            return False


    def compileReturn(self): 
        self.printOpenningXMLNameplate("returnStatement", "\t\t\t\t")
        self.printXMLNameplate("\t\t\t\t\t")
        self.tokenizer.advance()

        if (self.tokenizer.getToken() == ";"):
            self.printXMLNameplate("\t\t\t\t\t")
            self.printClosingXMLNameplate("returnStatement", "\t\t\t\t")
            self.tokenizer.advance()
        else:
            self.compileExpression()
            if (self.tokenizer.getToken() != ";"):
                self.errorMSG = "Method compileReturn(). Expected symbol ';' but {} was given".format(self.tokenizer.getToken())

                return False
            self.printXMLNameplate("\t\t\t\t\t")
            self.printClosingXMLNameplate("returnStatement", "\t\t\t\t")
            self.tokenizer.advance()



    def compileWhile(self):
        self.printOpenningXMLNameplate("whileStatement", "\t\t\t\t")
        self.printXMLNameplate("\t\t\t\t")  # print letStatement

        self.tokenizer.advance()

        if(self.tokenizer.getToken() != "("):
            self.errorMSG = "Method compileWhile(). Expected symbol '(' but {} was given".format(
                self.tokenizer.getToken())

            return False

        self.printXMLNameplate("\t\t\t\t")
        self.tokenizer.advance()

        self.compileExpression()

        if(self.tokenizer.getToken() != ")"):
            self.errorMSG = "Method compileWhile(). Expected symbol ')' but {} was given".format(self.tokenizer.getToken())
            return False

        self.printXMLNameplate("\t\t\t\t")
        self.tokenizer.advance()

        if(self.tokenizer.getToken() != "{"):
            self.errorMSG = "Method compileWhile(). Expected symbol '{{' but {} was given".format(self.tokenizer.getToken())

            return False
        
        self.printXMLNameplate("\t\t\t\t")
        self.tokenizer.advance()
        
        if(self.tokenizer.getToken() != "}"):

            if self.tokenizer.getToken() not in ["let", "if", "while", "do", "return"]:
                self.errorMSG = "Method compileWhile(). Expected statement  but {} was given".format(
                    self.tokenizer.getToken())

                return False
        
            while self.tokenizer.getToken() in ["let", "if", "while", "do", "return"]:
                self.compileStatements()
            

            if(self.tokenizer.getToken() != "}"):
                return False
            
            self.printXMLNameplate("\t\t\t\t")
            self.tokenizer.advance()


        else:
            self.printXMLNameplate("\t\t\t\t")
            self.tokenizer.advance()


        self.printClosingXMLNameplate("whileStatement", "\t\t\t\t")


    def compileLet(self): # apenas aceita esse formato -> let varName = expression ;
        self.printXMLNameplate("\t\t\t\t")  # print letStatement
        self.tokenizer.advance()
        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            self.errorMSG = "Method compileLet(). Expected identifier but {} was given".format(self.tokenizer.getToken())
            return False
        self.printXMLNameplate("\t\t\t\t")  # print varName
        self.tokenizer.advance()



        self.printXMLNameplate("\t\t\t\t")  # print =
        self.tokenizer.advance()

        self.compileExpression()


        if (self.tokenizer.getToken() != ";"):
            self.errorMSG = "Method compileLet(). Expected symbol ';' but {} was given".format(self.tokenizer.getToken())

            return False
        self.printXMLNameplate("\t\t\t\t")  # print =
        self.tokenizer.advance()

        self.printClosingXMLNameplate("letStatement", "\t\t\t\t")

    def compileIf(self):
        self.printOpenningXMLNameplate("ifStatement", "\t\t\t\t")
        self.printXMLNameplate("\t\t\t\t")
        self.tokenizer.advance()
        if (self.tokenizer.getToken() != "("):
            self.errorMSG = "Method compileIf(). Expected symbol '(' but {} was given".format(self.tokenizer.getToken())

            return False
        self.printXMLNameplate("\t\t\t\t\t")
        self.tokenizer.advance()
        self.compileExpression()
        
        if (self.tokenizer.getToken() != ")"):
            self.errorMSG = "Method compileIf(). Expected symbol ')' but {} was given".format(self.tokenizer.getToken())

            return False
        self.printXMLNameplate("\t\t\t\t\t")
        self.tokenizer.advance()


        if (self.tokenizer.getToken() != "{"):
            self.errorMSG = "Method compileIf(). Expected symbol '{{' but {} was given".format(self.tokenizer.getToken())
            return False

        self.printXMLNameplate("\t\t\t\t\t\t")
        self.tokenizer.advance()
        if self.tokenizer.getToken() not in ["let", "if", "while", "do", "return"]:
            self.errorMSG = "Method compileIf(). Expected statement but {} was given".format(self.tokenizer.getToken())

            return False
        
        while self.tokenizer.getToken() in ["let", "if", "while", "do", "return"]:
            self.compileStatements()

#            self.tokenizer.advance()


        if (self.tokenizer.getToken() != "}"):
            self.errorMSG = "Method compileIf(). Expected symbol '}}' but {} was given".format(self.tokenizer.getToken())
            return False

        self.printXMLNameplate("\t\t\t\t\t\t")

        self.tokenizer.advance()


        if (self.tokenizer.getToken() == "else"):
            self.printXMLNameplate("\t\t\t\t\t\t")
            self.tokenizer.advance()

            if (self.tokenizer.getToken() != "{"):
                return False
            self.printXMLNameplate("\t\t\t\t\t\t")

            self.tokenizer.advance()

            if self.tokenizer.getToken() not in ["let", "if", "while", "do", "return"]:
                if (self.tokenizer.getToken() == "}"):
                    self.printXMLNameplate("\t\t\t\t\t\t")
                    self.tokenizer.advance()
                    self.printClosingXMLNameplate("ifStatement", "\t\t\t\t")

                else:
                    self.errorMSG = "Method compileIf(). Expected symbol '}}' but {} was given".format(
                        self.tokenizer.getToken())
                    return False
            else:
                while self.tokenizer.getToken() in ["let", "if", "while", "do", "return"]:
                    self.compileStatements()
                #self.tokenizer.advance()

                if (self.tokenizer.getToken() != "}"):
                    self.errorMSG = "Method compileIf(). Expected symbol '}}' but {} was given".format(
                        self.tokenizer.getToken())

                    return False
                self.printXMLNameplate("\t\t\t\t\t\t")
                self.tokenizer.advance()

                self.printClosingXMLNameplate("ifStatement", "\t\t\t\t")
        else:
            self.printClosingXMLNameplate("ifStatement", "\t\t\t\t")
        


    def compileExpression(self):
        self.printOpenningXMLNameplate("expression", "\t\t\t\t")
        self.compileTerm()

        while (self.tokenizer.getToken() in ["+", "-", "*", "/", "&amp", "|", "&lt", "&gt", "="]):
            self.printXMLNameplate("\t\t\t\t\t") 
            self.tokenizer.advance()
            self.compileTerm()

        self.printClosingXMLNameplate("expression", "\t\t\t\t")

    def compileTerm(self):
        self.printOpenningXMLNameplate("term", "\t\t\t\t\t")
        
        aux = False
        if (self.tokenizer.tokenType() == self.tokenizer.INTEGER_CONSTANT):
            aux = True
            self.printXMLNameplate("\t\t\t\t\t\t") 
        elif (self.tokenizer.tokenType() == self.tokenizer.STRING_CONSTANT):
            aux = True
            self.printXMLNameplate("\t\t\t\t\t\t") 
        elif (self.tokenizer.KEYWORD):
            key = self.tokenizer.KEYWORD

            if key not in ("true", "false", "null", "this"):
                self.errorMSG = "Method compileTerm(). Expected keyword (true, false, null, this".format(
                    self.tokenizer.getToken())
                return False
            aux = True
            self.printXMLNameplate("\t\t\t\t\t\t")
        elif (self.tokenizer.getToken == "("):
            self.printXMLNameplate("\t\t\t\t\t\t")
            self.tokenizer.advance()
            self.compileExpression()

            if (self.tokenizer.getToken() != ")"):
                self.errorMSG = "Method compileTerm(). Expected symbol ')' but {} was given".format(self.tokenizer.getToken())
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
                    self.errorMSG = "Method compileTerm(). Expected symbol ']' but {} was given".format(
                        self.tokenizer.getToken())

                    return False
                
                aux = True
                self.printXMLNameplate("\t\t\t\t\t\t")

            elif (self.tokenizer.getToken() == "("):
                self.printXMLNameplate("\t\t\t\t\t\t")
                self.tokenizer.advance()
                #self.compileExpressionList()
                #todo compile expression list

                if (self.tokenizer.getToken() != ")"):
                    self.errorMSG = "Method compileTerm(). Expected symbol ')' but {} was given".format(
                        self.tokenizer.getToken())

                    return False
                
                aux = True
                self.printXMLNameplate("\t\t\t\t\t\t")

            elif (self.tokenizer.getToken() == "."):
                self.printXMLNameplate("\t\t\t\t\t\t")
                self.tokenizer.advance()

                if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                    self.errorMSG = "Method compileTerm(). Expected identifier but {} was given".format(
                        self.tokenizer.getToken())

                    return False

                self.printXMLNameplate("\t\t\t\t\t\t")
                self.tokenizer.advance()

                if (self.tokenizer.getToken() != "("):
                    self.errorMSG = "Method compileTerm(). Expected symbol '(' but {} was given".format(
                        self.tokenizer.getToken())

                    return False
                self.printXMLNameplate("\t\t\t\t\t\t")
                self.tokenizer.advance()
                #self.compileExpressionList

                if (self.tokenizer.getToken() != ")"):
                    self.errorMSG = "Method compileTerm(). Expected symbol ')' but {} was given".format(
                        self.tokenizer.getToken())

                    return False
                self.printXMLNameplate("\t\t\t\t\t\t")
                self.tokenizer.advance()
        if aux == True:
            self.tokenizer.advance()
        self.printClosingXMLNameplate("term", "\t\t\t\t\t")
