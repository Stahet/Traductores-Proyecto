#!/usr/bin/env python
# -*- coding: utf-8 -*-'''
from  sys import argv as argumentos_consola
import ply.lex as lexi
import expresiones


def salir(mensaje = "ERROR: Ejecute el interprete de la forma: setlan <dir_archivo>",
                codigo = -1):
    print mensaje
    exit(codigo)
    

def analizar_archivo(ruta_archivo):
    
    analizador = lexi.lex(module = expresiones)
    
    try:
        with open(ruta_archivo) as entrada:
            analizador.input(entrada.read())
    except IOError as e :
        salir(e + "\nError: Compruebe que el archivo existe o tiene permisos de lectura")
    
    return analizador
        


def setlan(argv = None):
         
    if argv is None:
        argv = argumentos_consola
        
    if len(argv) != 2:
        salir()
        
    ruta_archivo = argv[1]
    analizar_archivo(ruta_archivo)
    expresiones.LAST_FILE = ruta_archivo
    if not expresiones.ERROR_:
        import parser

        
    expresiones.ERROR_ = False
 
if __name__ == '__main__':
        
    setlan(['setlan','casos_parser/caso1.txt'])
    
else:
    print "¡No lo importe!"
    salir()
