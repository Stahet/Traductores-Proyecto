# -*- coding: utf-8 -*-'''
'''
Created on 4/2/2015

@author: Jonnathan Ng    11-10199
         Manuel Gonzalez 11-10399
'''
import ply.yacc as yacc
import ply.lex as lexi

import expresiones
from AST import *

tokens = expresiones.tokens

def p_expression_binary(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression INTDIVISION expression
                  | expression RESTDIVISION expression 
                  | expression TIMES expression'''
    p[0] = BinaryIntOp(p[1],p[2],p[3])        

def p_expression_unary(p):
    '''expression : MINUS expression'''
    p[0] = UnaryIntOp(p[1],p[2])
    
def p_integer(p):
    '''expression : INTEGER'''
    p[0] = Int(p[1])



files = open('casos_parser/caso1.txt')
lexer = lexi.lex(module=expresiones)
parser = yacc.yacc()
print parser.parse(files.read())
#a = []
files.close()
