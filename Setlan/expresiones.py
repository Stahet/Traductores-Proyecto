# -*- coding: utf-8 -*-'''
'''
Created on 19/1/2015

@author: manuggz
'''

from tokens import *

ERROR_ = False

    # Palabras reservadas
reservadas = {
   'if' : ('IF',TokenProgram),
   'then' : ('THEN',TokenProgram),
   'else' : ('ELSE',TokenProgram),
   'while' : ('WHILE',TokenProgram),
   'program':('PROGRAM',TokenProgram),
   'int' :('INT',TokenProgram),
   'bool':('BOOL',TokenProgram),
   'set':('SET',TokenProgram),
}

simbolos = {
   '{' : ('CORCHETE_AB',TokenOpenCurly),
   '}' : ('CORCHETE_CE',TokenCloseCurly),
   ';' : ('PUNTO_COMA',TokenSemicolon),
   ',' : ('COMA',TokenComma),
   '=':('IGUAL',TokenEquals),
   '*' :('MULTI',TokenAsterisk),
   '+':('SUMA',TokenPlus),
   '-':('GUION',TokenDash),
   '/' : ('INT_DIVISION' , TokenIntegerDivision),
   '%' : ('RESTO' , TokenRestDivision),
   '\\': ('COUNTER_SLASH',TokenCounterSlash),
   '<' : ('MAYOR',TokenGreater),
   '>' : ('MENOR',TokenLess),
   '@' : ('CONCA_CONJUNTOS',TokenConcatSets),
   '(' : ('PARENTESIS_AB',TokenOpenParenthesis),
   ')' : ('PARENTESIS_CE',TokenCloseParenthesis),
    ':' : ('DOS_PUNTOS',TokenColon)
}

op_mapeados = {
   '<+>' : ('MAP_SUMA',TokenMapSuma),
   '<->' : ('MAP_RESTA',TokenMapSubstract),
   '<*>' : ('MAP_MULTI',TokenMapMulti),
   '</>' : ('MAP_DIVISION',TokenMapIntDivision),
   '<%>':('MAP_REST',TokenMapRest),
}

unarios_conjuntos = {
   '<?' : ('MAX_VALOR', TokenMaxValorSet),
   '>?' : ('MIN_VALOR', TokenMinValorSet),
   '$?' : ('NUM_ELEMEN',TokenSizeSet),
}

simbolos_igual = {
   '<=' : ('MENOR_O_IGUAL', TokenLessOrEqual),
   '>=' : ('MAYOR_O_IGUAL', TokenGreaterOrEqual),
   '==' : ('DOBLE_IGUAL',TokenEqualBool),
   '/=' : ('DISTINTO_DE',TokenDifferent),
}

tokens = ['ID' , 'SIMBOLO' , 'MAPEADO','DOUBLE_PLUS' , 'UNARIO_CONJUNTO',\
          'SIMBOLOS_CON_IGUAL','INTERSECCION','FLECHA']  + \
         [i[0] for i in reservadas.values()]  + \
         [i[0] for i in simbolos.values()]    + \
         [i[0] for i in op_mapeados.values()] + \
         [i[0] for i in unarios_conjuntos.values()] 


t_ignore = ' \t'

def t_INTERSECCION(t):
    '><'
    t.value = (t.value ,TokenInterseccion(t))
    return t

def t_FLECHA(t):
    '->'
    t.value = (t.value ,TokenArrow(t))
    return t

def t_SIMBOLOS_CON_IGUAL(t):
    r'[><=/]='
    valor = simbolos_igual[t.value]
    t.type = valor[0]    # Check for reserved words
    t.value = (t.value,valor[1](t))
    return t
    

def t_UNARIO_CONJUNTO(t):
    r'[<>\$]\?'
    valor = unarios_conjuntos[t.value]
    t.type = valor[0]    # Check for reserved words
    t.value = (t.value,valor[1](t))
    return t

def t_MAPEADO(t):
    r'<[\+\-\*/%]>'
    valor = op_mapeados[t.value]
    t.type = valor[0]    # Check for reserved words
    t.value = (t.value,valor[1](t))
    return t

def t_DOUBLE_PLUS(t):
    r'\+\+'
    t.value = (t.value,TokenDoublePlus(t))
    return t

def t_SIMBOLO(t):
    r'[{};,=\*\+\-/%\\<>@\(\):]'
    valor = simbolos[t.value]
    t.type = valor[0]    # Check for reserved words
    t.value = (t.value,valor[1](t))
    return t


def t_ID(t):
    r'[a-zA-Z][a-zA-Z\d_]*'
    
    valor = reservadas.get(t.value,('ID',TokenID))
    t.type = valor[0]    # Check for reserved words
    t.value = (t.value,valor[1](t))
    return t

def t_COMMENTARIO(t):
    r'\#.*'
    pass

def t_nueva_linea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)    

# Manejador de errores
def t_error(t):
    global ERROR_
    tok = Token(t)
    print('Error: se encontró  un caracter inesperado "%s" en la línea %d, Columna %d.' % (tok.valor,tok.linea,tok.obtener_columna()))
    tok.analizador.skip(1)
    ERROR_ = True
