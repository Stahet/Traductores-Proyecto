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


def p_program(p):
    'program : PROGRAM statement'
    p[0] = Program(p[1],p[2])
    

def p_statement_assing(p):
    '''statement : IDENTIFIER ASSIGN expression'''
    p[0] = Assign(p[1],p[3])
    
def p_statement_block(p):
    '''statement : LCURLY declare statement_list RCURLY '''
    p[0] = Block(p[2],p[3])

def p_statement_function(p):
    '''statement : SCAN IDENTIFIER 
                 | PRINT   comma_list
                 | PRINTLN comma_list'''
    
    p[0] = FunctionBuiltIn(p[1],p[2])

def p_expression_dato(p):
    '''expression : INTEGER
            | FALSE
            | TRUE
            | STRING
            | IDENTIFIER
    '''
    p[0] = p[1]

def p_expression_parent(p):
    ''' expression : LPARENT expression RPARENT'''
    p[0] = Parenthesis(p[2])

def p_expression_curly(p):
    ''' expression : LCURLY expression RCURLY'''
    p[0] = Block(p[2])

def p_expression_op_bin(p):
    '''expression : expression PLUS expression            
                 | expression MINUS expression            
                 | expression TIMES expression            
                 | expression INTDIVISION expression            
                 | expression RESTDIVISION expression            
                 | expression '==' expression
                 | expression '/=' expression
                 | expression '<' expression
                 | expression '<=' expression
                 | expression '>' expression
                 | expression '>=' expression
                 | expression '@' expression
                 | expression '++' expression
                 | expression '\' expression
                 | expression '><' expression
                 | expression '<+>' expression
                 | expression '<->' expression
                 | expression '<*>' expression
                 | expression '</>' expression
                 | expression '<%>' expression
    '''
    
    p[0] = BinaryOP(p[1],p[2],p[3])
    
def p_expression_op_unary(p):
    '''expression : '-' expression
                  | >? expression
                  | <? expression
                  | $? expression'''
    p[0] = UnaryOP(p[1],p[2])
    
def p_comma_list_expression(p):
    '''comma_list : expression'''
    p[0] = p[1]
    
def p_comma_list_expression_comma_continue(p):
    '''comma_list : expression , comma_list'''
    p[0] = SeparetedTerms(p[1],p[2],p[3])
    
def p_statement_list(p):
    '''statement_list : statement'''
    p[0] = p[1]
    
def p_statement_list_continue(p):
    '''statement_list : statement ; statement_list'''
    p[0] = SeparetedTerms(p[1],p[2],p[3])

def p_declare_vars(p):
    '''declare : USING declare_list IN '''
    p[0] = p[2]

def p_declare_empty(p):
    '''declare :empty'''
    pass

def p_declare_list_type(p):
    '''declare_list : type IDENTIFIER declare_list_continue'''
    p[0] = DeclareList(p[1],p[2],p[3])

def p_declare_list_(p):
    '''declare_list : declare_list ; declare_list'''
    p[1].declared_list = p[1].declared_list + p[3].declared_list
    p[0] = p[1]

def p_declare_list_continue_end(p):
    '''declare_list_continue : ;'''
    p[0] = []

def p_declare_list_continue_on(p):
    '''declare_list_continue : , IDENTIFIER declare_list_continue'''
    p[0] = [p[2]] + [p[3]]

def p_direction_all(p):
    ''''direction : min
                  | max
    '''
    p[0] = p[1]

def p_type_data(p):
    '''type: 'int' 
           | 'bool'
           | 'set'
    '''
    p[0] = p[1]

# Precedence defined for expressions
precedence = (
    # language
    ("right", 'IF'),
    ("right", 'ELSE'),
    # bool
    ("left", 'OR'),
    ("left", 'AND'),
    ("right", 'NOT'),
    # compare
    ("nonassoc", 'BELONG'),
    ("nonassoc", 'EQUAL', 'UNEQUAL'),
    ("nonassoc", 'LESS', 'LESSEQ', 'GREAT', 'GREATEQ'),
    # range
    ("left", 'INTERSECTION'),
    # int
    ("left", 'PLUS', 'MINUS'),
    ("left", 'TIMES', 'DIVIDE', 'MODULO'),
    # range
    ("nonassoc", 'FROMTO'),
    # int
    ("right", 'UMINUS'),
)
    
files = open('casos_parser/caso1.txt')
lexer = lexi.lex(module=expresiones)
parser = yacc.yacc()
print parser.parse(files.read())
#a = []
files.close()
