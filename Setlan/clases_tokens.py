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
    '''
        classdocs
    '''

    def __init__(self, t):
        '''
        Constructor
        '''
        Token.__init__(self, t)
        
    def __str__(self):
        return "TokenProgram(Línea %d , Columna %d)" % (self.t.lineno,self.obtener_columna())
        