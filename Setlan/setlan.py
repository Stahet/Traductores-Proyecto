#!/usr/bin/env python
# -*- coding: utf-8 -*-'''
from  sys import argv as argumentos_consola
import ply.lex as lexi
import expresiones



def setlan():
    
    analizador = lexi.lex(module = expresiones)
    
    if len(argumentos_consola) != 2:
        print("ERROR: Ejecute el interprete de la forma: setlan <dir_archivo>")
        exit(-1)
    
    try:
        with open(argumentos_consola[1]) as entrada:
            analizador.input(entrada.read())
            entrada.close()
    except IOError as e :
        print(e)
        print("Error: Compruebe que el archivo existe o tiene permisos de lectura")
        exit(-1)
        
    for token in analizador:  # @UndefinedVariable
        print token.type,
        if token.type in ('TokenID',''):
            print "\"" + token.value + "\"" ,
        print "(Línea %d , Columna %d)" % (token.lineno,expresiones.obtener_columna(token))

if __name__ == '__main__':
    setlan()
else:
    print("¡No lo importe!")
    print("ERROR: Ejecute el interprete de la forma: setlan <dir_archivo>")
    exit(-1)