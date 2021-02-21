import re

class JackTokenizer:
    p = re.compile('".*"|[a-zA-Z_]+[a-zA-Z0-9_]*|[0-9]+|[+|*|/|\-|{|}|(|)|\[|\]|\.|,|;|<|>|=|~|&]')

    identifierPattern = "[a-zA-Z_]+[a-zA-Z0-9_]*"
    integerPattern = "[0-9]+"
    stringPattern = '".*"'
    symbolsPattern = "|[+|*|/|\-|{|}|(|)|\[|\]|\.|,|;|<|>|=|~]"
    commandsArray = [
        "class", "constructor", "function", "method", "field", "static",
        "var", "int", "char", "boolean", "void", "true", "false", "null",
        "this", "let", "do", "if", "else", "while", "return"
    ]
    symbolsArray = [
        "{", "}", "(", ")", "[", "]",
        ".", ",", ";", "+", "-", "*", "/",
        "&", "|", "<", ">", "=", "~"
    ]

    def __init__ (self, filePath):
        self.file = open(filePath, "r").read()
        self.tokens = p.findall(self.file)
        self.tokenIndex = 0

    def hasMoreTokens(self):
        return self.tokenIndex <= len(self.tokens)-1

    def advance(self):
        if (self.hasMoreTokens()):
            self.tokenIndex += 1
    
    def replacingSymbol(self, symbol):
        if (symbol == "<"):
            return "&lt"
        elif (symbol == ">"):
            return "&gt"
        elif (symbol == '"'):
            return "&quot"
        elif (symbol == == '&'):
            return "&amp"
        else: 
            return symbol

    def tokenType(self, token):
        if (re.match(self.identifierPattern, token)):
            if (token in self.commandsArray):
                return "<keyword> {} </keyword>".format(token)
            else :
                return "<identifier> {} </identifier>".format(token)
        elif (re.match(self.integerPattern, token)):
            return "<integerConstant> {} </integerConstant>".format(token)
        elif (re.match(self.stringPattern, token)):
            return "<stringConstant> {} </stringConstant>".format(token[1:len(token)-1])
        elif (re.match(self.symbolsPattern, token)):
            return "<symbol> {} </symbol> ".format(self.symbolReplace(token))
        else:
            return "<unidentifiedToken> {} </unidentifiedToken> ".format(token)


    def analyzer(self):
        file = open("result.txt", "w")
        print("<tokens>", file=file)
        
        while self.hasMoreTokens():
            print(self.tokenType(self.tokens[self.tokenIndex]), file=file)

            self.advance()

        print("</tokens>", file=file)
        file.close()