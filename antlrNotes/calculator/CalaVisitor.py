# Generated from Cala.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CalaParser import CalaParser
else:
    from CalaParser import CalaParser

# This class defines a complete generic visitor for a parse tree produced by CalaParser.

class CalaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CalaParser#prog.
    def visitProg(self, ctx:CalaParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalaParser#printExpr.
    def visitPrintExpr(self, ctx:CalaParser.PrintExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalaParser#assign.
    def visitAssign(self, ctx:CalaParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalaParser#blank.
    def visitBlank(self, ctx:CalaParser.BlankContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalaParser#parens.
    def visitParens(self, ctx:CalaParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalaParser#MulDiv.
    def visitMulDiv(self, ctx:CalaParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalaParser#AddSub.
    def visitAddSub(self, ctx:CalaParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalaParser#id.
    def visitId(self, ctx:CalaParser.IdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalaParser#int.
    def visitInt(self, ctx:CalaParser.IntContext):
        return self.visitChildren(ctx)



del CalaParser