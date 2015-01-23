# -*- coding: utf-8 -*-'''
'''
Created on 19/1/2015

@author: manuggz
'''


ERROR_ = False


# Palabras reservadas
reservadas = {
   'if' : 'IF',
   'then': 'THEN',
   'else' : 'ELSE',
   'while' :'WHILE',
   'program':'PROGRAM',
   'int' :'INT',
   'bool':'BOOL',
   'set':'SET',
}

simbolos = {
   '{' :'TokenOpenCurly',
   '}' :'TokenCloseCurly',
   ';' :'TokenSemicolon',
   ',' :'TokenComma',
   '=' :'TokenEquals',
   '*' :'TokenAsterisk',
   '+' :'TokenPlus',
   '-' :'TokenDash',
   '/' :'TokenIntegerDivision',
   '%' :'TokenRestDivision',
   '\\':'TokenCounterSlash',
   '<' :'TokenGreater',
   '>' :'TokenLess',
   '@' :'TokenConcatSets',
   '(' :'TokenOpenParenthesis',
   ')' :'TokenCloseParenthesis',
    ':' :'TokenColon'
}

op_mapeados = {
   '<+>':'TokenMapSuma',
   '<->':'TokenMapSubstract',
   '<*>':'TokenMapMulti',
   '</>':'TokenMapIntDivision',
   '<%>':'TokenMapRest',
}

unarios_conjuntos = {
   '<?' :'TokenMaxValorSet',
   '>?' :'TokenMinValorSet',
   '$?' :'TokenSizeSet',
}

simbolos_igual = {
   '<=' :'TokenLessOrEqual',
   '>=' :'TokenGreaterOrEqual',
   '==' :'TokenEqualBool',
   '/=' :'TokenDifferent',
}

tokens = ['TokenID' , 'SIMBOLO' , 'MAPEADO','TokenDoublePlus' , 'UNARIO_CONJUNTO',\
          'SIMBOLOS_CON_IGUAL','TokenInterseccion','TokenArrow']  + reservadas.values() + \
         simbolos.values() + op_mapeados.values() + \
         unarios_conjuntos.values()


t_ignore = ' \t'

def t_TokenInterseccion(t):
    '><'
    return t

def t_TokenArrow(t):
    '->'
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

def t_ToukenDoublePlus(t):
    r'\+\+'
    return t

def t_SIMBOLO(t):
    r'[{};,=\*\+\-/%\\<>@\(\):]'
    valor = simbolos[t.value]
    t.type = valor    # Check for reserved words
    return t


def t_TokenID(t):
    r'[a-zA-Z][a-zA-Z\d_]*'    
    valor = reservadas.get(t.value,'TokenID')
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
    
    ultimo_salto = token.lexer.lexdata.rfind('\n',0,token.lexpos)
    if ultimo_salto < 0:
        ultimo_salto = 0
    columna = (token.lexpos - ultimo_salto) + (token.lineno == 1)
    
    return columna

# Manejador de errores
def t_error(t):
    global ERROR_

    print('Error: se encontró  un caracter inesperado "%s" en la línea %d, Columna %d.' % (t.value,t.lineno,obtener_columna(t)))
    t.lexer.skip(1)
    ERROR_ = True
