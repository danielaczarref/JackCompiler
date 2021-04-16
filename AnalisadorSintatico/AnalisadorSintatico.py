from JackTokenizer.JackTokenizer import JackTokenizer
from CodeGenerator.symbol import SymbolTable
from CodeGenerator.CodeWriter import  CodeWriter
import re




class AnalisadorSintatico:

    def __init__(self, input_file_name):
        self.tokenizer = JackTokenizer(input_file_name)
        self.input_file_name = input_file_name
        self.symbolTable = SymbolTable()
        self.className = None

        self.codeWriter = CodeWriter(input_file_name)

        self.if_counter = 0
        self.while_counter = 0

        self.kind_myd = {
            "FIELD" : "THIS",
            "ARG" : "ARG",
            "STATIC" : "STATIC",
            "VAR" : "LOCAL"
        }
        self.operator_myd = {
            '+' : 'ADD',
            '-' : 'SUB',
            '&amp' : 'AND',
            '|' : 'OR',
            '&lt' : 'LT',
            '&gt' : 'GT',
            '=' : 'EQ'
        }


    def compile(self):
        self.compileClass()
        # if(self.compileClass()):
            # self.codeWriter.close()
        # else:
            # self.codeWriter.close()



    def compileClass(self):

        # if(self.tokenizer.getToken() != "class"):
        #     self.errorMSG = "Method compileClass(). Expected keyword class but {} was given".format(self.tokenizer.getToken())
        #     return False  # não é uma classe pois esperavamos a keyword "classe" aqui

        self.tokenizer.advance() # class

        self.className = self.tokenizer.getToken()

        self.tokenizer.advance() # className


        self.tokenizer.advance()  # {

        while (self.tokenizer.getToken() in ["static", "field"]):
            self.compileClassVarDec()

        while (self.tokenizer.getToken() in ["method", "constructor", "function"]):
            self.compileSubroutineDec()


        self.tokenizer.advance() # }

        # print(len(self.codeWriter.output))


        # with open(self.input_file_name.split(".")[0]+".vm", 'w') as f:
        #     f.write('\n'.join(self.codeWriter.output))


    def compileClassVarDec(self):

        kind = self.tokenizer.getToken().upper()

        self.tokenizer.advance() # static ou field

        tipo = self.tokenizer.getToken()

        self.tokenizer.advance() # type

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception

        self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)

        self.tokenizer.advance()  # type

        while self.tokenizer.getToken() != ';':

            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                raise Exception
            self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
            self.tokenizer.advance()

        self.tokenizer.advance()

    def compileSubroutineDec(self):
        self.symbolTable.clear()

        subRoutineType = self.tokenizer.getToken()

        if(subRoutineType == "method"):
            self.symbolTable.addElement("this", self.className, "ARG")

        self.tokenizer.advance() # method, constructor, function


        self.tokenizer.advance()  # type

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception

        method_name = "{}.{}".format(self.className, self.tokenizer.getToken())

        self.tokenizer.advance()  # identifier

        self.tokenizer.advance()  # (

        self.compileParameterList()

        self.tokenizer.advance()  # )

        self.tokenizer.advance()  # {

        while self.tokenizer.getToken() == "var":
            self.compileVarDec()

        args_counter = self.symbolTable.getCount("VAR")

        self.codeWriter.writeFunction(method_name, args_counter)

        if(subRoutineType == "method"):
            self.codeWriter.push("ARG", 0)
            self.codeWriter.pop("POINTER", 0)
        elif(subRoutineType == "constructor"):
            field_counter = self.symbolTable.getCount("FIELD")
            self.codeWriter.push("CONST", field_counter)
            self.codeWriter.writeCall("Memory.alloc", 1)
            self.codeWriter.pop("POINTER", 0)



        self.compileStatements()

        self.tokenizer.advance()  # }

        # self.symbolTable.printSubroutineTable("Subroutine {}".format(class_name))

    def compileParameterList(self):

        kind = "ARG"

        if(self.tokenizer.getToken() == ")"):
            return

        tipo = self.tokenizer.getToken()
        self.tokenizer.advance()  # type

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception("Esperava identificador")

        self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)

        self.tokenizer.advance()  # identifier

        while self.tokenizer.getToken() != ")":
            self.tokenizer.advance()  # ,

            tipo = self.tokenizer.getToken()

            self.tokenizer.advance()  #

            if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                raise Exception("Esperava identificador")
            self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
            self.tokenizer.advance()  #



    def compileVarDec(self):

        self.tokenizer.advance()  #var

        kind = "VAR"
        tipo = self.tokenizer.getToken()

        self.tokenizer.advance()  # type

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception
        self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
        self.tokenizer.advance()  # identifier

        while self.tokenizer.getToken() != ";":
            self.tokenizer.advance()  # t,
            if (self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                raise Exception
            self.symbolTable.addElement(self.tokenizer.getToken(), tipo, kind)
            self.tokenizer.advance()  #

        self.tokenizer.advance()  #




    def compileStatements(self):

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

    def compileIf(self):

        self.tokenizer.advance()  # if

        self.tokenizer.advance()  # (

        self.compileExpression()

        self.tokenizer.advance()  # )

        label_1 = "IF_TRUE{}".format(self.if_counter)
        label_2 = "IF_FALSE{}".format(self.if_counter)
        label_3 = "IF_END{}".format(self.if_counter)

        self.codeWriter.writeIfGoto(label_1)
        self.codeWriter.writeGoto(label_2)
        self.codeWriter.writeLabel(label_1)
        self.if_counter += 1


        self.tokenizer.advance()  # {

        self.compileStatements()

        self.codeWriter.writeGoto(label_3)

        self.tokenizer.advance()  # }
        self.codeWriter.writeLabel(label_2)

        if(self.tokenizer.getToken() == "else"):
            self.tokenizer.advance() # else
            self.tokenizer.advance() # {
            self.compileStatements()
            self.tokenizer.advance() # }
        self.codeWriter.writeLabel(label_3)

    def compileWhile(self):

        self.tokenizer.advance()  # while

        label_1 = "WHILE_EXP{}".format(self.while_counter)
        label_2 = "WHILE_END{}".format(self.while_counter)
        self.while_counter += 1
        self.codeWriter.writeLabel(label_1)


        self.tokenizer.advance()  # (

        self.compileExpression()
        self.codeWriter.writeExpression("NOT")
        self.tokenizer.advance()  # )

        self.tokenizer.advance()  # {

        self.codeWriter.writeIfGoto(label_2)
        self.compileStatements()

        self.codeWriter.writeGoto(label_1)
        self.codeWriter.writeLabel(label_2)

        self.tokenizer.advance()  # }



    def compileLet(self):

        self.tokenizer.advance()  # let

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception


        tipo, categ, pos = self.symbolTable.get(self.tokenizer.getToken())
        # print(categ)
        categoria = self.kind_myd[categ]


        self.tokenizer.advance()  # identifier



        if(self.tokenizer.getToken() == "["):
            self.tokenizer.advance() # [

            self.compileExpression()

            self.tokenizer.advance()  # ]

            self.codeWriter.push(categoria, pos)
            self.codeWriter.writeExpression("ADD")
            self.codeWriter.pop("TEMP", 0)


            self.tokenizer.advance()  # =

            self.compileExpression()

            self.codeWriter.push("TEMP", 0)
            self.codeWriter.pop("POINTER", 1)
            self.codeWriter.pop("THAT", 0)


        else:

            self.tokenizer.advance()  # =

            self.compileExpression()
            self.codeWriter.pop(categoria, pos)

        self.tokenizer.advance()  # ;
        return True

    def compileReturn(self):
        self.tokenizer.advance()  # return

        if(self.tokenizer.getToken() != ";"):
            self.compileExpression()
        else:
            self.codeWriter.push("CONST", 0)
        self.codeWriter.writeReturn()
        self.tokenizer.advance()  # ;

    def compileDo(self):
        self.tokenizer.advance()  # do

        if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
            raise Exception

        variable_name = self.tokenizer.getToken()
        self.tokenizer.advance()  # identifier

        self.compileSubroutineCall(variable_name)
        self.codeWriter.pop("TEMP", 0)

        self.tokenizer.advance()  # ;


    def compileExpression(self):
        self.compileTerm()
        print("operator {}".format(self.tokenizer.getToken()))

        while (self.tokenizer.getToken() in ['+', '-' , '&amp', '|', '&lt', '&gt', '=' ]):
            operation = self.tokenizer.getToken()
            self.tokenizer.advance()  # ,

            self.compileTerm()
            if(operation in self.operator_myd):
                self.codeWriter.writeExpression(self.operator_myd.get(operation))
            elif (operation == "*"):
                self.codeWriter.writeCall("Math.multiply", 2)
            elif (operation == "/"):
                self.codeWriter.writeCall("Math.divide", 2)
            else:
                raise Exception

        return True

    def compileExpressionList(self):

        len_args = 0

        if(self.tokenizer.getToken() == ")"):
            return len_args

        self.compileExpression()
        len_args = len_args + 1

        while (self.tokenizer.getToken() != ")"):

            self.tokenizer.advance()  # ,
            self.compileExpression()
            len_args = len_args + 1


        return len_args

    def compileSubroutineCall(self, variable_name):

        functionName = variable_name
        args_counter = 0

        if(self.tokenizer.getToken() == "."):
            self.tokenizer.advance()  # .
            subroutineName = self.tokenizer.getToken()

            self.tokenizer.advance()  # identifier

            tipo, categ, pos = self.symbolTable.get(variable_name)

            if(tipo != None):
                categoria = self.kind_myd[categ]

                self.codeWriter.push(categoria, pos)
                functionName = "{}.{}".format(tipo, subroutineName)
                args_counter += 1
            else:
                functionName = "{}.{}".format(variable_name, subroutineName)

        elif (self.tokenizer.getToken() == "("):
            subroutineName = variable_name
            functionName = "{}.{}".format(self.className, subroutineName)
            args_counter += 1
            self.codeWriter.push("POINTER", 0)

        self.tokenizer.advance()  # (

        args_counter += self.compileExpressionList()

        self.tokenizer.advance()  # )
        self.codeWriter.writeCall(functionName, args_counter)


    def compileString(self):
        string = self.tokenizer.getToken[1:]

        self.codeWriter.push("CONST", len(string))
        self.codeWriter.writeCall("String.new", 1)

        for i in string:
            self.codeWriter.push("CONST", ord(i))
            self.codeWriter.writeCall("String.appendChar", 2)


        self.tokenizer.advance()  # string

    def compileTerm(self):

        if(self.tokenizer.tokenType() == self.tokenizer.STRING_CONSTANT):
            self.compileString()
        elif(self.tokenizer.tokenType() == self.tokenizer.INTEGER_CONSTANT):
            self.codeWriter.push("CONST", int(self.tokenizer.getToken()))
            self.tokenizer.advance()  # int

        elif(self.tokenizer.getToken() in ["false", "null", "true"]):
            self.codeWriter.push("CONST", 0)
            if(self.tokenizer.getToken() == "true"):
                self.codeWriter.writeExpression("NOT")

            self.tokenizer.advance()  # keyword

        elif(self.tokenizer.getToken() == "this"):
            self.codeWriter.push("POINTER", 0)

            self.tokenizer.advance()  # this

        elif(self.tokenizer.getToken() in ["-", "~"]):
            op = self.tokenizer.getToken()

            self.tokenizer.advance()  #

            self.compileTerm()
            if(op == "-"):
                self.codeWriter.writeExpression("NEG")
            else:
                self.codeWriter.writeExpression("NOT")

        elif(self.tokenizer.getToken() == "("):

            self.tokenizer.advance()  # (

            self.compileExpression()

            self.tokenizer.advance()  # )
        else:
            if(self.tokenizer.tokenType() != self.tokenizer.IDENTIFIER):
                raise Exception

            varName = self.tokenizer.getToken()

            self.tokenizer.advance()  # identifier

            if(self.tokenizer.getToken() == "["):
                self.tokenizer.advance()  # [
                self.compileExpression()
                self.tokenizer.advance()  # ]

                tipo, categ, pos = self.symbolTable.get(varName)
                category = self.kind_myd[categ]
                self.codeWriter.push(category, pos)
                self.codeWriter.writeExpression("ADD")
                self.codeWriter.pop("POINTER", 1)
                self.codeWriter.push("THAT", 0)


            elif(self.tokenizer.getToken() in [".", "("]):
                self.compileSubroutineCall(varName)
            else:
                tipo, categ, pos = self.symbolTable.get(varName)
                category = self.kind_myd[categ]
                self.codeWriter.push(category, pos)


