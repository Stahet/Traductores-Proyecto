# -*- coding: utf-8 -*-'''
'''
Created on 19/1/2015

@author: manuggz
'''


ERROR_ = False


# Palabras reservadas
reservadas = {
   'program':'PROGRAM',
   'using' : 'USING',
   'in' : 'IN',
   'if' : 'IF',
   'then': 'THEN',
   'else' : 'ELSE',
   'for' : 'FOR',
   'do' : 'DO',
   'min' : 'MIN',
   'max' : 'MAX',
   'repeat'  :  'REPEAT',
   'while' :'WHILE',
   'int' :'INT',
   'set':'SET',
   'bool':'BOOL',
   'and' :'AND',
   'or'  :'OR',
   'not' :'NOT',
   'scan':'SCAN',
   'println':'PRINTLN'
}

booleanos = {
   'true' : 'TRUE',
   'false': 'FALSE'
}

simbolos = {
   '{' :'LCURLY',
   '}' :'RCURLY',
   ';' :'SEMICOLON',
   ',' :'COMMA',
   '=' :'EQUALS',
   '*' :'ASTERISK',
   '+' :'PLUS',
   '-' :'DASH',
   '/' :'INTDIVISION',
   '%' :'RESTDIVISION',
   '\\':'COUNTERSLASH',
   '<' :'GREATERTHAN',
   '>' :'LESSTHAN',
   '@' :'CONCATSETS',
   '(' :'LPARENTHESIS',
   ')' :'RPARENTHESIS',
   '$' :'asd',
    ':' :'COLON'
}

op_mapeados = {
   '<+>':'MAPSUM',
   '<->':'MAPSUBSTRACT',
   '<*>':'MAPMULTI',
   '</>':'MAPINTDIVISION',
   '<%>':'MAPREST',
}

unarios_conjuntos = {
   '<?' :'MAXVALORSET',
   '>?' :'MINVALORSET',
   '$?' :'SIZESET',
}

simbolos_igual = {
   '<=' :'LESSOREQUALTHAN',
   '>=' :'GREATEROREQUALTHAN',
   '==' :'EQUALBOOL',
   '/=' :'DIFFERENT',
}

tokens = ['IDENTIFIER', 'INTEGER', 'SIMBOLO' , 'MAPEADO','DOUBLEPLUS' , 'UNARIO_CONJUNTO',\
          'SIMBOLOS_CON_IGUAL','INTERSECCION','ARROW','STRING']  + reservadas.values() + \
         simbolos.values() + op_mapeados.values() + \
         unarios_conjuntos.values() + booleanos.values() + \
         simbolos_igual.values()


t_ignore = ' \t'

def t_STRING(t):
    r'".*"'
    return t

def t_INTEGER(t):
    r'[0-9]+'
    return t

def t_booleanos(t):
    r'true|false'
    t.type = booleanos[t.value]
    return t

def t_INTERSECCION(t):        
    r'><'
    return t

def t_ARROW(t):
    r'->'
    return t

def t_SIMBOLOS_CON_IGUAL(t):
    r'[><=/]='
    valor = simbolos_igual[t.value]
    t.type = valor    # Check for reserved words
    return t
    
def t_UNARIO_CONJUNTO(t):
    r'[<>\$]\?'
    valor = unarios_conjuntos[t.value]
    t.type = valor    # Check for reserved words
    return t

def t_MAPEADO(t):
    r'<[\+\-\*/%]>'
    valor = op_mapeados[t.value]
    t.type = valor    # Check for reserved words
    return t

def t_DOUBLEPLUS(t):
    r'\+\+'
    return t

def t_SIMBOLO(t):
    r'[{};,=\*\+\-/%\\<>@\(\):$]'
    valor = simbolos[t.value]
    t.type = valor    # Check for reserved words
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z\d_]*'    
    valor = reservadas.get(t.value,'IDENTIFIER')
    t.type = valor    # Check for reserved words
    return t

def t_COMMENTARIO(t):
    r'\#.*'
    pass

def t_nueva_linea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)    

# Encuentra la columna 
#     token instancia del token    
def obtener_columna(token):
    'Encuentra la columna del token'
    ultimo_salto = token.lexer.lexdata.rfind('\n',0,token.lexpos)  # ultima posicion del salto de linea
    if ultimo_salto < 0:
        ultimo_salto = 0
    columna = (token.lexpos - ultimo_salto) + (token.lineno == 1)
    
    return columna

# Manejador de errores
def t_error(t):
    global ERROR_
    print('Error: se encontró  un caracter inesperado "%s" en la línea %d, Columna %d.' % (t.value,t.lineno,obtener_columna(t)))
    ERROR_ = True
    t.lexer.skip(1)
