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

    KEYWORD = "keyword"
    IDENTIFIER = "identifier"
    INTEGER_CONSTANT = "integerConstant"
    STRING_CONSTANT = "stringConstant"
    SYMBOL = "symbol"
    UNIDENTIFIED_TOKEN = "unidentifiedToken"

    def __init__(self, filePath):
        self.file = open(filePath, "r").read()
        self.tokens = self.p.findall(self.file)
        self.tokenIndex = 0

    def hasMoreTokens(self):
        return self.tokenIndex <= len(self.tokens) - 1

    def advance(self):
        if (self.hasMoreTokens()):
            self.tokenIndex += 1

    def getToken(self):
        return self.replaceSymbol(self.tokens[self.tokenIndex])

    def peekToken(self):
        return self.replaceSymbol(self.tokens[self.tokenIndex + 1])

    def replaceSymbol(self, symbol):
        if (symbol == "<"):
            return "&lt"
        elif (symbol == ">"):
            return "&gt"
        elif (symbol == '"'):
            return "&quot"
        elif (symbol == '&'):
            return "&amp"
        else:
            return symbol

    def tokenType(self):
        token = self.getToken()
        if (re.match(self.identifierPattern, token)):
            if (token in self.commandsArray):
                return self.KEYWORD
            else:
                return self.IDENTIFIER
        elif (re.match(self.integerPattern, token)):
            return self.INTEGER_CONSTANT
        elif (re.match(self.stringPattern, token)):
            return self.STRING_CONSTANT
        elif (re.match(self.symbolsPattern, token)):
            return self.SYMBOL
        else:
            return self.UNIDENTIFIED_TOKEN

    def peekTokenType(self):
        token = self.peekToken()
        if (re.match(self.identifierPattern, token)):
            if (token in self.commandsArray):
                return self.KEYWORD
            else:
                return self.IDENTIFIER
        elif (re.match(self.integerPattern, token)):
            return self.INTEGER_CONSTANT
        elif (re.match(self.stringPattern, token)):
            return self.STRING_CONSTANT
        elif (re.match(self.symbolsPattern, token)):
            return self.SYMBOL
        else:
            return self.UNIDENTIFIED_TOKEN