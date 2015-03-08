#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 23/2/2015

@author: Jonnathan Ng    11-10199
         Manuel Gonzalez 11-10399
         
         Archivo principal de Setlan
         Para Ejecutar:  setlan <nombre archivo> <flags>
         Flags: -
'''
from  sys import argv as argumentos_consola
from AST import static_errors
import expresiones
import parse
import ply.lex as lexi

def setlan(argv = None):
    # Abrir ruta del archivo   
    if argv is None:
        argv = argumentos_consola
        
    if len(argv) < 2:
        salir()
     
    ruta_archivo = argv[1]
    try:
        with open(ruta_archivo) as file_input:
            content = file_input.read()
            content = content.expandtabs(4)
            expresiones.cont_archivo = content
    except IOError as e :
        salir(str(e) + "\nError: Compruebe que el archivo existe o tiene permisos de lectura")
        
    lexer = expresiones.build_lexer()           # Construir Lexer
    tree = parse.build_parser(content,lexer) # Contruimos el Parser
    
    # Impresion de errores
    if expresiones.lexer_errors:
        for error in expresiones.lexer_errors:
            print error
            return
        
    elif parse.parser_errors:
        for error in parse.parser_errors:
            print error
            return
    
    else: # Pasa el lexer y el parser
        tree.check_types() # Hacemos el chequeo estatico 
        # Impresion de errores
        if static_errors:
            for error in static_errors:
                print "Error en la linea %d, columna %d: %s" % \
                       (error[0],expresiones.obtener_columna_texto_lexpos(error[1]),error[2])
            return
    
    # Pasan los errores pasamos a interpretar    
    if "-t" in argv:
        print "####################       LISTA DE TOKENS      ####################\n" 
        expresiones.print_tokens(expresiones.build_lexer(), content)
    
    if "-a" in argv:
        print "\n#################### ARBOL SINTACTICO ABSTRACTO ####################\n" 
        tree.print_tree()
    
    if "-s" in argv:
        print "\n####################      CHEQUEO DE TIPOS       ####################\n" 
        print tree.symbolTable.str
    
    tree.execute()
def salir(mensaje = "ERROR: Ejecute el interprete de la forma: setlan <dir_archivo> [-t] [-a] [-s]",
                codigo = -1):
    print mensaje
    exit(codigo)    
             
if __name__ == '__main__':
    #setlan()
    #setlan(["setlan","casos_check/2ContextoIgualNombre.stl","-t","-s","-a"])
    #setlan(["setlan","casos_check/3variables.stl","-t","-s","-a"])
    #setlan(["setlan","casos_check/all.stl","-t","-s","-a"])
    #setlan(["setlan","casos_check/conjuntoVacio.stl","-t","-s","-a"])
    #setlan(["setlan","casos_check/enunciadoError2.stl","-t","-s","-a"])
    #setlan(["setlan","casos_check/erroresOperadores","-t","-s","-a"])
    #setlan(["setlan","casos_check/errorFor","-t","-s","-a"])
    #setlan(["setlan","casos_check/errorIf","-t","-s","-a"])
    #setlan(["setlan","casos_check/errorRepeatWhile","-t","-s","-a"])
    #setlan(["setlan","casos_check/errorScan.stl","-t","-s","-a"])
    #setlan(["setlan","casos_check/errorWhile","-t","-s","-a"])
    #setlan(["setlan","casos_check/escrituraIterador.stl","-t","-s","-a"])
    #setlan(["setlan","casos_check/operacionesConConjuntos.stl","-t","-s","-a"])
    #setlan(["setlan","casos_check/reglasDeAlcance.stl","-t","-s","-a"])
    #setlan(["setlan","casos_check/terrible.stl","-t","-s","-a"])
    #setlan(["setlan","casos_check/test1.stl","-t","-s","-a"])
    #setlan(["setlan","casos_check/test2EnunciadoErrorTipo.stl","-t","-s","-a"])
    #setlan(["setlan","casos_check/variableNoDeclarada","-t","-s","-a"])
    
    ####### Interpretador
    #setlan(["setlan","casos_interpretador/guardar_variables","-t","-s","-a"])
    #setlan(["setlan","casos_interpretador/conjuntoEnteros","-t","-s","-a"])
    #setlan(["setlan","casos_interpretador/booleanos","-t","-s","-a"])
    setlan(["setlan","casos_interpretador/pruebaScan","-t","-s","-a"])