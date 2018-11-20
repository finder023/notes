#!/usr/bin/env python3

from CalaParser import CalaParser
from CalaVisitor import CalaVisitor

class MyVisitor(CalaVisitor):
    def __init__(self):
        self.memory = {}

    def visitAssign(self, ctx:CalaParser.AssignContext):
        key = ctx.ID().getText()
        val = self.visit(ctx.expr())
        self.memory[key] = val
        return val

    def visitPrintExpr(self, ctx:CalaParser.PrintExprContext):
        val = self.visit(ctx.expr())
        print(val)
        return 0

    def visitInt(self, ctx:CalaParser.IntContext):
        return ctx.INT().getText()

    def visitId(self, ctx:CalaParser.IdContext):
        key = ctx.ID().getText()
        if key in self.memory:
            return self.memory[key]
        return 0

    
    def visitAddSub(self, ctx:CalaParser.AddSubContext):
        left = int(self.visit(ctx.expr(0)))
        right = int(self.visit(ctx.expr(1)))

        if ctx.op.type == CalaParser.ADD:
            return left + right
        return left - right

    def visitMulDiv(self, ctx:CalaParser.MulDivContext):
        left = int(self.visit(ctx.expr(0)))
        right = int(self.visit(ctx.expr(1)))

        if ctx.op.type == CalaParser.MUL:
            return left * right
        return left / right
    
    def visitParens(self, ctx:CalaParser.ParensContext):
        return self.visit(ctx.expr())