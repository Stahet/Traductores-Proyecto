# -*- coding: utf-8 -*-'''
'''
Created on 4/2/2015

@author: Jonnathan Ng    11-10199
         Manuel Gonzalez 11-10399
'''
import ply.yacc as yacc
from expresiones import tokens
from AST import *
from expresiones import LAST_FILE


def p_expression_binary(p):
    '''expression : expression PLUS expression
                  | expression DASH expression
                  | expression INTDIVISION expression
                  | expression RESTDIVISION expression 
                  | expression ASTERISK expression'''
    p[0] = BinaryIntOp(p[1],p[2],p[3])        

def p_expression_unary(p):
    '''expression : DASH expression'''
    p[0] = UnaryIntOp(p[1],p[2])
    
def p_integer(p):
    '''expression : INTEGER'''
    p[0] = Int(p[1])
    
#import ply.lex as lexi

#files = open('casos/caso4.txt')
#lexer = lexi.lex(module=expresiones)
parser = yacc.yacc()
input_file = open(LAST_FILE)
print parser.parse(input_file.read())
input_file.close()



