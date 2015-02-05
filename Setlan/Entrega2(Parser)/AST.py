# -*- coding: utf-8 -*-'''
'''
Created on 4/2/2015

@author: Jonathan Ng 11-10199
         Manuel Gonzalez 11-10390
'''

class Expre:pass

class Program(Expre):
    ''' Representa los numeros enteros'''
    def __init__(self, statement):
        self.type = "PROGRAM"
        self.statement = statement

class Assign(Expre):
    def __init__(self, identifier,expresion):
        self.type = "ASSIGN"
        self.id = identifier
        self.expresion = expresion

class Block(Expre):
    def __init__(self, list_ex,declare = None):
        self.type = "BLOCK"
        self.list_ex = list_ex
        self.declare = declare

class FunctionBuiltIn(Expre):
    def __init__(self, type_f,to_print):
        self.type_f = type_f
        self.to_print = to_print

class Parenthesis(Expre):
    def __init__(self, expre):
        self.type = 'PARENTHESIS'
        self.expre = expre
        
class BinaryOP(Expre):
    def __init__(self, type_op,op1,op2):
        self.type_op = type_op
        self.op1  = op1
        self.op2  = op2

class UnaryOP(Expre):
    def __init__(self, type_op,op1):
        self.type_op = type_op
        self.op1  = op1

class SeparetedTerms(Expre):
    def __init__(self, op1,sep,op2):
        self.op1  = op1
        self.sep = sep
        self.op2  = op1

class DeclareList(Expre):
    def __init__(self,type_d,identifier,continue_l):
        self.declared_list= []
        self.declared_list.append((type_d,identifier,continue_l))
    
    def __add__(self,c):