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
parser_errores = []

def p_program(p):
    'program : PROGRAM statement'
    p[0] = Program(p[2])
    
def p_statement_assing(p):
    'statement : IDENTIFIER ASSIGN expression'
    p[0] = Assign(p[1],p[3])
    
def p_statement_block(p):
    'statement : LCURLY declare statement_list RCURLY'
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

def p_statement_list_empty(p):
    'statement_list : empty'
    p[0] = []
    
def p_declare_vars(p):
    'declare : USING declare_list IN'
    p[0] = DeclareList(p[2])

def p_declare_empty(p):
    'declare : empty'
    pass
    
def p_declare_list_type(p):
    'declare_list : type identifier_list SEMICOLON declare_list'
    p[0] = [TypeList(p[1],p[2])] + p[4]
    
def p_declare_list_type_empty(p):
    'declare_list : empty'
    p[0] = []

def p_identifier_list(p):
    'identifier_list : IDENTIFIER'
    p[0] = [p[1]]

def p_declare_list_continue_on(p):
    'identifier_list : IDENTIFIER COMMA identifier_list'
    p[0] = [p[1]] + p[3]

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
    global parser_errores
    if parser_errores: return
    
    if p:
        msg = 'Error de síntaxis en la línea %d , columna %d. '
        msg += 'Token inesperado "%s".'
        value = p.value
        try:
            value = p.value[0]
        except TypeError:
            pass
        
        msg = msg % (p.lineno , expresiones.obtener_columna(p) , value)
    else:
        msg = 'Error de síntasis: Alcanzado final de archivo inesperadamente.'

    parser_errores.append(msg)
    
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
#file_input = open('casos_parser/all.txt')
#file_input = open('casos_parser/programa_vacio.txt')
#file_input = open('casos_parser/fibonacci.txt')
#file_input = open('casos_parser/usingInVacio.txt')
#file_input = open('casos_parser/holaMundo.txt')
#file_input = open('casos_parser/operacionesConConjuntos.txt')
#file_input = open('casos_parser/precedenciaIF.txt')
#file_input = open('casos_parser/errorDeSintaxis.txt')  # Falta Mejorar Manejo de errores
#file_input = open('casos_parser/reglasDeAlcance.txt')
file_input = open('casos_lexer/caso10.txt')

content = file_input.read()
content = content.expandtabs(5)
file_input.close()


lexer.errores  = []
#lexer.input(content)
program = parser.parse(content,lexer)
if lexer.errores:
    for error in lexer.errores:
        print error
    
elif parser_errores:
    for error in parser_errores:
        print error
else:
    program.print_tree()
    
file_input.close()