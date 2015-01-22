# -*- coding: utf-8 -*-'''
'''
Created on 19/1/2015

@author: manuggz
'''

class Token():
    
    
    def __init__(self,t):
        self.t = t
        self.linea = t.lineno
        self.valor = t.value[0]
        self.columna = -1
        self.analizador = self.t.lexer
    
    # Encuentra la columna 
    #     token instancia del token
    
    
    def obtener_columna(self):
        'Encuentra la columna del token'
        
        if self.columna == -1:
            ultimo_salto = self.t.lexer.lexdata.rfind('\n',0,self.t.lexpos)
            if ultimo_salto < 0:
                ultimo_salto = 0
            self.columna = (self.t.lexpos - ultimo_salto) + (self.t.lineno == 1)

        return self.columna
    

class TokenProgram(Token):
    def __str__(self):
        return "TokenProgram(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenID(Token):
    def __str__(self):
        return "TokenID: \"" + str(self.t.value[0]) + "\"(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenOpenCurly(Token):
    def __str__(self):
        return "TokenOpenCurly(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenCloseCurly(Token):
    def __str__(self):
        return "TokenCloseCurly(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())
    
class TokenSemicolon(Token):
    def __str__(self):
        return "TokenSemicolon(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenComma(Token):
    def __str__(self):
        return "TokenComma(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenEquals(Token):
    def __str__(self):
        return "TokenEquals(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenMulti(Token):
    def __str__(self):
        return "TokenMulti(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenPlus(Token):
    def __str__(self):
        return "TokenPlus(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenSubstract(Token):
    def __str__(self):
        return "TokenSubstract(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

        