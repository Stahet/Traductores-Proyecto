'''
Created on 4/2/2015

@author: Jonnathan
'''

class Int:
    ''' Representa los numeros enteros'''
    def __init__(self, value):
        self.type = "integer"
        self.value = value

class BinaryIntOp:
    ''' Representa las operaciones binarias de enteros'''
    def __init__(self,left,operator,right):
        self.type = "binOp"
        self.left = left
        self.right = right
        self.operator = operator
        
class UnaryIntOp:
    ''' Representa el operador unario de enteros'''
    def __init__(self,operator,value):
        self.type = "unary"
        self.operator = operator
        self.value = value
