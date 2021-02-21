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