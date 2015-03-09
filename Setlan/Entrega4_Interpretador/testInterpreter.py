'''
Created on 8/3/2015

@author: Jonathan Ng 11-10199
         Manuel Gonzalez 11-10390
'''
import unittest

from setlan import setlan
from AST import interpreter_result

class InterpreterTestSuite(unittest.TestCase):
    def tearDown(self):
        del interpreter_result[:]
        
    def testBoolean(self):
        self.assertEqual(setlan(["setlan","casos_interpretador/booleanos"]).strip(), open('casos_interpretador/respuestas/booleanos.txt','r').read().strip())
    
    def testEnteros(self):
        self.assertEqual(setlan(["setlan","casos_interpretador/conjuntoEnteros"]).strip(), open('casos_interpretador/respuestas/conjuntoEnteros.txt','r').read().strip())
    
    def testGuardarVariables(self):
        self.assertEqual(setlan(["setlan","casos_interpretador/guardar_variables"]).strip(), open('casos_interpretador/respuestas/guardar_variables.txt','r').read().strip())
    
    def testWhileDo(self):
        self.assertEqual(setlan(["setlan","casos_interpretador/pruebaWhileDo"]).strip(), open('casos_interpretador/respuestas/pruebaWhileDo.txt','r').read().strip())
    
    def testForMalicia(self):
        self.assertEqual(setlan(["setlan","casos_interpretador/testForMalicia"]).strip(), open('casos_interpretador/respuestas/testForMalicia.txt','r').read().strip())
    
    def testPruebaFor(self):
        self.assertEqual(setlan(["setlan","casos_interpretador/pruebaFor"]).strip(), open('casos_interpretador/respuestas/pruebaFor.txt','r').read().strip())
    
    def testPruebaIf(self):
        self.assertEqual(setlan(["setlan","casos_interpretador/pruebaIf"]).strip(), open('casos_interpretador/respuestas/pruebaIf.txt','r').read().strip())
    
    def testMaliciaFor(self):
        self.assertEqual(setlan(["setlan","casos_interpretador/pruebaMaliciaFor"]).strip(), open('casos_interpretador/respuestas/pruebaMaliciaFor.txt','r').read().strip())
    
    def testReglasALcance(self):
        self.assertEqual(setlan(["setlan","casos_interpretador/reglasDeAlcance"]).strip(), open('casos_interpretador/respuestas/reglasDeAlcance.txt','r').read().strip())  

    def testOperacionesConj(self):
        self.assertEqual(setlan(["setlan","casos_interpretador/testOperacionesConjuntos"]).strip(), open('casos_interpretador/respuestas/testOperacionesConjuntos.txt','r').read().strip()) 
    
    def testRepeatWhileDo(self):
        self.assertEqual(setlan(["setlan","casos_interpretador/testRepeatWhileDo"]).strip(), open('casos_interpretador/respuestas/testRepeatWhileDo.txt','r').read().strip()) 
if __name__ == "__main__":
    unittest.main()