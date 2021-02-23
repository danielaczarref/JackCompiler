from JackTokenizer import JackTokenizer

j = JackTokenizer("main.jack")

while j.hasMoreTokens():
    print("{} -> {}".format(j.tokenType(), j.getToken()))

    j.advance()

