from AnalisadorSintatico.AnalisadorSintatico import AnalisadorSintatico
import sys
import os



for i in range(1, len(sys.argv)):
   a = AnalisadorSintatico(sys.argv[i])
   a.compile()

