#!/usr/bin/env python3

import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from CalaLexer import CalaLexer
from CalaParser import CalaParser
from myVisitor import MyVisitor

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(sys.stdin.readline())

    lexer = CalaLexer(input_stream)
    tokenStream = CommonTokenStream(lexer)
    parser = CalaParser(tokenStream)

    tree = parser.prog()

    visitor = MyVisitor()
    visitor.visit(tree)