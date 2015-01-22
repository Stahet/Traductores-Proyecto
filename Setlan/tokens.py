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

class TokenPlus(Token):
    def __str__(self):
        return "TokenPlus(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenAsterisk(Token):
    def __str__(self):
        return "TokenAsterisk(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenDash(Token):
    def __str__(self):
        return "TokenDash(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenIntegerDivision(Token):
    def __str__(self):
        return "TokenIntegerDivision(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenRestDivision(Token):
    def __str__(self):
        return "TokenRestDivision(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenCounterSlash(Token):
    def __str__(self):
        return "TokenCounterSlash(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenGreater(Token):
    def __str__(self):
        return "TokenGreater(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenLess(Token):
    def __str__(self):
        return "TokenLess(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenConcatSets(Token):
    def __str__(self):
        return "TokenConcatSets(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenOpenParenthesis(Token):
    def __str__(self):
        return "TokenOpenParenthesis(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenCloseParenthesis(Token):
    def __str__(self):
        return "TokenCloseParenthesis(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenColon(Token):
    def __str__(self):
        return "TokenColon(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenMapSuma(Token):
    def __str__(self):
        return "TokenMapSuma(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenMapSubstract(Token):
    def __str__(self):
        return "TokenMapSubstract(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenMapMulti(Token):
    def __str__(self):
        return "TokenMapMulti(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenMapIntDivision(Token):
    def __str__(self):
        return "TokenMapIntDivision(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenMapRest(Token):
    def __str__(self):
        return "TokenMapRest(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenMaxValorSet(Token):
    def __str__(self):
        return "TokenMaxValorSet(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenMinValorSet(Token):
    def __str__(self):
        return "TokenMinValorSet(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenSizeSet(Token):
    def __str__(self):
        return "TokenSizeSet(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenLessOrEqual(Token):
    def __str__(self):
        return "TokenLessOrEqual(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenGreaterOrEqual(Token):
    def __str__(self):
        return "TokenGreaterOrEqual(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenEqualBool(Token):
    def __str__(self):
        return "TokenEqualBool(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenDifferent(Token):
    def __str__(self):
        return "TokenDifferent(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenInterseccion(Token):
    def __str__(self):
        return "TokenInterseccion(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenArrow(Token):
    def __str__(self):
        return "TokenArrow(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

class TokenDoublePlus(Token):
    def __str__(self):
        return "TokenDoublePlus(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())

