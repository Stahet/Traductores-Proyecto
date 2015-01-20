# -*- coding: utf-8 -*-'''
'''
Created on 19/1/2015

@author: manuggz
'''

from clases_tokens import *

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
   'set':('SET',TokenProgram)
}

tokens = ['ID'] + [i[0] for i in reservadas.values()]


t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-Z][a-zA_Z\d_]*'
    
    valor = reservadas.get(t.value,('ID',TokenProgram))
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
