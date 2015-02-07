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
_error_parser = False

def p_program(p):
    'program : PROGRAM statement'
    p[0] = Program(p[2])
    
def p_statement_assing(p):
    'statement : IDENTIFIER ASSIGN expression'
    p[0] = Assign(p[1],p[3])
    
def p_statement_block(p):
    'statement : LCURLY declare statement_list RCURLY '
    p[0] = Block(p[3],p[2])

def p_statement_function_scan(p):
    'statement : SCAN IDENTIFIER'
    p[0] = Scan(Identifier(p[2]))
    
def p_statement_function_print(p):
    'statement : PRINT comma_list'
    p[0] = Print(p[1],[p[2]])
    
def p_statement_function_println(p):
    'statement : PRINTLN comma_list'
    p[0] = Print(p[1],[p[2], '\n'])
    
def p_statement_if(p):
    '''statement : IF LPARENT expression RPARENT statement ELSE statement
                 | IF LPARENT expression RPARENT statement '''
    if len(p) == 8:
        p[0] = If(p[3],p[5],p[7])
    else:
        p[0] = If(p[3],p[5])
    
def p_statement_for(p):
    'statement :  FOR IDENTIFIER direction expression DO statement'
    p[0] = For(Identifier(p[2]),p[3],p[4],p[6])
    
def p_statement_repeat_while_do(p):
    'statement :  REPEAT statement WHILE LPARENT expression RPARENT DO statement'
    p[0] = RepeatWhileDo(p[2],p[5],p[8])
    
def p_statement_while_do(p):
    'statement :  WHILE LPARENT expression RPARENT DO statement'
    p[0] = WhileDo(p[3],p[6])
    
def p_statement_repeat_while(p):
    'statement :  REPEAT statement WHILE LPARENT expression RPARENT'
    p[0] = RepeatWhile(p[2],p[5])

def p_expression_bool(p):
    '''expression : FALSE
                  | TRUE
    '''
    p[0] = Bool(p[1])
    
def p_expression_direction(p):
    '''direction : MIN
                  | MAX
    '''
    p[0] = Direction(p[1])
    
def p_expression_int(p):
    'expression : INTEGER'
    p[0] = Integer(p[1])

def p_expression_string(p):
    'expression : STRING'
    p[0] = String(p[1])

def p_expression_id(p):
    'expression : IDENTIFIER'
    p[0] = Identifier(p[1])

def p_expression_parent(p):
    ''' expression : LPARENT expression RPARENT'''
    p[0] = Parenthesis(p[2])

def p_expression_set(p):
    ''' expression : LCURLY comma_list RCURLY'''
    p[0] = Set(p[2])

def p_expression_op_set(p):
    '''expression : expression DOUBLEPLUS expression
                 | expression COUNTERSLASH expression
                 | expression INTERSECCION expression
    '''
    operadores = {
        '++' : 'DOUBLEPLUS',
        '\\' : 'COUNTERSLASH',
        '><' : 'INTERSECCION'
    }
    p[0] = BinaryOP(p[1],\
                    operadores[p[2]]  + ' ' + p[2]\
                    ,p[3])

def p_expression_op_bin_compare(p):
    '''expression : expression EQUALBOOL expression
                 | expression UNEQUAL expression
                 | expression LESSTHAN expression
                 | expression LESSOREQUALTHAN expression
                 | expression GREATERTHAN expression
                 | expression GREATEROREQUALTHAN expression
                 | expression BELONG expression
    '''
    p[0] = BinaryOP(p[1],\
                    expresiones.simbolos.get(p[2],expresiones.simbolos_igual.get(p[2],None))  + ' ' + p[2]\
                    ,p[3])

def p_expression_op_bin_map_to_set(p):
    '''expression : expression MAPPLUS expression
                 | expression MAPMINUS expression
                 | expression MAPTIMES expression
                 | expression MAPDIVIDE expression
                 | expression MAPREST expression
    '''
    
    p[0] = BinaryOP(p[1],expresiones.op_mapeados[p[2]]  + ' ' + p[2]\
                    ,p[3])
    
def p_expression_op_bin_integer(p):
    '''expression : expression PLUS expression            
                 | expression MINUS expression            
                 | expression TIMES expression            
                 | expression INTDIVISION expression            
                 | expression RESTDIVISION expression            
    '''
    
    p[0] = BinaryOP(p[1],expresiones.simbolos[p[2]]  + ' ' + p[2]\
                    ,p[3])

def p_expression_op_bin_bool(p):
    '''expression : expression AND expression
                  | expression OR expression '''
    
    p[0] = BinaryOP(p[1],expresiones.reservadas[p[2]]  + ' ' + p[2]\
                    ,p[3])
    
def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = UnaryOP(p[1],p[2])
    
def p_expression_op_unary(p):
    '''expression : NOT expression
                  | MAXVALUESET expression
                  | MINVALUESET expression
                  | SIZESET expression'''
    p[0] = UnaryOP(p[1],p[2])

def p_comma_list_expression(p):
    'comma_list : expression'
    p[0] = [p[1]]
    
def p_comma_list_expression_comma_continue(p):
    'comma_list : expression COMMA comma_list'
    p[0] = [p[1]] + p[3]
    
def p_statement_list_continue(p):
    'statement_list : statement SEMICOLON statement_list'
    p[0] = [p[1]] + p[3]


def p_statement_list(p):
    'statement_list : statement SEMICOLON'
    p[0] = [p[1]]
    
def p_declare_vars(p):
    'declare : USING declare_list IN '
    p[0] = p[2]

def p_declare_empty(p):
    'declare : empty'
    pass

def p_declare_list_type(p):
    'declare_list : type IDENTIFIER declare_list_continue'
    p[0] = DeclareList(p[1],p[2],p[3])

def p_declare_list_(p):
    'declare_list : declare_list SEMICOLON declare_list'
    p[1].declared_list = p[1].declared_list + p[3].declared_list
    p[0] = p[1]

def p_declare_list_continue_end(p):
    'declare_list_continue : SEMICOLON'
    p[0] = []

def p_declare_list_continue_on(p):
    'declare_list_continue : COMMA IDENTIFIER declare_list_continue'
    p[0] = [p[2]] + p[3]

def p_empty(p):
    'empty :'
    pass

def p_type_data(p):
    '''type : INT
           | BOOL
           | SET
    '''
    p[0] = p[1]
    
def p_error(p):
    global _error_parser
    
    if _error_parser: return
    
    try:
        print 'Error: se encontró  un caracter inesperado "%s" en la línea %d, Columna %d.' % (p.value[0] , p.lineno , expresiones.obtener_columna(p))
    except TypeError:
        print 'Error: se encontró  un caracter inesperado "%s" en la línea %d, Columna %d.' % (p.value , p.lineno , expresiones.obtener_columna(p))
    _error_parser = True
    
# Precedence defined for expressions
precedence = (
    # language
    ("right", 'IF'  ),
    ("right", 'ELSE'),
    # bool
    ("left", 'OR'),
    ("left", 'AND'),
    ("right", 'NOT'),
    # compare
    ("nonassoc", 'LESSTHAN', 'LESSOREQUALTHAN', 'GREATERTHAN', 'GREATEROREQUALTHAN'),
    ("nonassoc", 'EQUALBOOL', 'UNEQUAL'),
    ("nonassoc", 'BELONG'),
    # int
    ("left", 'PLUS', 'MINUS'),
    ("left", 'TIMES', 'INTDIVISION', 'RESTDIVISION'),
    #set
    ('left','DOUBLEPLUS','COUNTERSLASH'),
    ('left','INTERSECCION'),
    #map to set
    ('left','MAPPLUS','MAPMINUS'),
    ('left','MAPTIMES','MAPDIVIDE','MAPREST'),
    #unary over sets
    ('nonassoc','MAXVALUESET','MINVALUESET','SIZESET'),
    # int
    ("right", 'UMINUS'),
)

lexer = lexi.lex(module=expresiones)
parser = yacc.yacc()

#file_input = open('casos_lexer/caso1.txt')
file_input = open('casos_parser/all.txt')
content = file_input.read()
file_input.close()

#lexer.input(content)
if expresiones.ERROR_:
    exit(-1)
    
program = parser.parse(content)
if not _error_parser:
    program.print_tree()
file_input.close()
