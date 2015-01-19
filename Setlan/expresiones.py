# -*- coding: utf-8 -*-'''
'''
Created on 19/1/2015

@author: manuggz
'''
import ply.lex as lexi

variables_reservadas =['program','int','set','bool']

tokens = ['PROGRAM','IDENTIFICADOR','TIPO_INT','SALTO']


t_ignore = ' \t'
t_PROGRAM = 'program'
t_IDENTIFICADOR = r'[a-zA-Z][a-zA_Z\d_]*'
t_TIPO_INT = 'int'
t_SALTO = r'\n'

def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)    

# Manejador de errores
def t_error(t):
    print('Error: se encontró  un caracter inesperado "%s" en la línea %d, Columna %d.' % (t.value[0],t.lineno,t.lexpos))
    t.lexer.skip(1)
    
analizador = lexi.lex()
