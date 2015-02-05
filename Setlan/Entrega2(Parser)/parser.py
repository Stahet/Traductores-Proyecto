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
    'PROGRAM : PROGRAM STATEMENT'
    p[0] = Program(p[1],p[2])        

def p_statement_assing(p):
    '''STATEMENT : IDENTIFIER ASSIGN EXPRESSION'''
    p[0] = Assign(p[1],p[3])
    
def p_statement_block(p):
    '''STATEMENT : LCURLY DECLARE STATEMENT_LIST RCURLY '''
    p[0] = Block(p[2],p[3])

def p_statement_function(p):
    '''STATEMENT : SCAN IDENTIFIER 
                 | PRINT   COMMA_LIST
                 | PRINTLN COMMA_LIST'''
    
    p[0] = FunctionBuiltIn(p[1],p[2])

def p_expression_dato(p):
    '''EXPRESSION : INTEGER
            | FALSE
            | TRUE
            | STRING
            | IDENTIFIER
    '''
    p[0] = p[1]

def p_expression_parent(p):
    ''' EXPRESSION : LPARENT EXPRESSION RPARENT'''
    p[0] = Parenthesis(p[2])

def p_expression_curly(p):
    ''' EXPRESSION : LCURLY EXPRESSION RCURLY'''
    p[0] = Block(p[2])

def p_expression_op_bin(p):
    '''EXPRESSION:EXPRESSION '+' EXPRESSION            
                 | EXPRESSION '-' EXPRESSION            
                 | EXPRESSION '*' EXPRESSION            
                 | EXPRESSION '/' EXPRESSION            
                 | EXPRESSION '%' EXPRESSION            
                 | EXPRESSION '==' EXPRESSION
                 | EXPRESSION '/=' EXPRESSION
                 | EXPRESSION '<' EXPRESSION
                 | EXPRESSION '<=' EXPRESSION
                 | EXPRESSION '>' EXPRESSION
                 | EXPRESSION '>=' EXPRESSION
                 | EXPRESSION '@' EXPRESSION
                 | EXPRESSION '++' EXPRESSION
                 | EXPRESSION '\' EXPRESSION
                 | EXPRESSION '><' EXPRESSION
                 | EXPRESSION '<+>' EXPRESSION
                 | EXPRESSION '<->' EXPRESSION
                 | EXPRESSION '<*>' EXPRESSION
                 | EXPRESSION '</>' EXPRESSION
                 | EXPRESSION '<%>' EXPRESSION
    '''
    
    p[0] = BinaryOP(p[1],p[2],p[3])
    
def p_expression_op_unary(p):
    '''EXPRESSION : '-' EXPRESSION
                  | >? EXPRESSION
                  | <? EXPRESSION
                  | $? EXPRESSION'''
    p[0] = UnaryOP(p[1],p[2])
    
def p_comma_list_expression(p):
    '''COMMA_LIST : EXPRESSION'''
    p[0] = p[1]
    
def p_comma_list_expression_comma_continue(p):
    '''COMMA_LIST : EXPRESSION , COMMA_LIST'''
    p[0] = SeparetedTerms(p[1],p[2],p[3])
    
def p_statement_list(p):
    '''STATEMENT_LIST : STATEMENT'''
    p[0] = p[1]
    
def p_statement_list_continue(p):
    '''STATEMENT_LIST : STATEMENT ; STATEMENT_LIST'''
    p[0] = SeparetedTerms(p[1],p[2],p[3])

def p_declare_vars(p):
    '''DECLARE : 'using' DECLARE_LIST 'in' '''
    p[0] = p[2]

def p_declare_empty(p):
    '''DECLARE :EMPTY'''
    pass

def p_declare_list_type(p):
    '''DECLARE_LIST : TYPE 'identifier' DECLARE_LIST_CONTINUE'''
    p[0] = DeclareList(p[1],p[2],p[3])

def p_declare_list_(p):
    '''DECLARE_LIST : DECLARE_LIST ; DECLARE_LIST'''
    p[1].declared_list = p[1].declared_list + p[3].declared_list
    p[0] = p[1]

def p_declare_list_continue_end(p):
    '''DECLARE_LIST_CONTINUE: ;'''
    p[0] = []

def p_declare_list_continue_on(p):
    '''DECLARE_LIST_CONTINUE: , IDENTIFIER DECLARE_LIST_CONTINUE'''
    p[0] = [p[2]] + [p[3]]

def p_direction_all(p):
    ''''DIRECTION : min
                  | max
    '''
    p[0] = p[1]

def p_type_data(p):
    '''TYPE: 'int' 
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
