#!/usr/bin/env python
# -*- coding: utf-8 -*-'''
from  sys import argv as argumentos_consola
import ply.lex as lexi
import expresiones

def setlan(argv = None):
     
    analizador = lexi.lex(module = expresiones)
    
    if argv is None:
        if len(argumentos_consola) != 2:
            print "ERROR: Ejecute el interprete de la forma: setlan <dir_archivo>"
            exit(-1)
        argv = argumentos_consola
     
    try:
        with open(argv[1]) as entrada:
            analizador.input(entrada.read())
            entrada.close()
    except IOError as e :
        print e
        print "Error: Compruebe que el archivo existe o tiene permisos de lectura"
        exit(-1)
     
    tokens = []
    for token in analizador:
        tokens.append(token)
     
     
    if not expresiones.ERROR_:
        for token in tokens:
            print 'token',token.type,' '*(20 - len(token.type)),
            print "value (" + str(token.value) + ") at line ",token.lineno,\
                 ", column " , expresiones.obtener_columna(token)
    
    expresiones.ERROR_ = False
 
if __name__ == '__main__':
    print('caso1')
    setlan(['setlan','casos_lexer/caso1.txt'])
    print('caso2')
    setlan(['setlan','casos_lexer/caso2.txt'])
    print('caso3')
    setlan(['setlan','casos_lexer/caso3.txt'])
    print('caso4')
    setlan(['setlan','casos_lexer/caso4.txt'])
    print('caso5')
    setlan(['setlan','casos_lexer/caso5.txt'])
    print('caso6')
    setlan(['setlan','casos_lexer/caso6.txt'])
    print('caso7')
    setlan(['setlan','casos_lexer/caso7.txt'])
    print('caso8')
    setlan(['setlan','casos_lexer/caso8.txt'])
    print('caso9')
    setlan(['setlan','casos_lexer/caso9.txt'])
    print('caso10')
    setlan(['setlan','casos_lexer/caso10.txt'])
    print('caso11')
    setlan(['setlan','casos_lexer/caso11.txt'])
    print('caso12')
    setlan(['setlan','casos_lexer/caso12.txt'])
    print('caso13')
    setlan(['setlan','casos_lexer/caso13.txt'])
else:
    print "¡No lo importe!"
    print "ERROR: Ejecute el interprete de la forma: setlan <dir_archivo>"
    exit(-1)
