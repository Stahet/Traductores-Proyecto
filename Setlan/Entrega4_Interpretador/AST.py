# -*- coding: utf-8 -*-'''
'''
Created on 4/2/2015

@author: Jonathan Ng 11-10199
         Manuel Gonzalez 11-10390
    
    Clases para la representación de un Arbol abstracto del lenguaje setlan
'''

from symbol_table import SymbolTable
from expresiones import obtener_columna_texto_lexpos
from functions import *

global static_errors
static_errors = []

class Expre:
    
    def __init__(self):
        self.lexpos = -1
        self.lineno = -1
    
    def get_indent_number(self,level):
        return level * 4
    
    def get_ident_str(self,level):
        return self.get_indent_number(level) * r" "
    
    def print_with_indent(self,cad,level):
        print self.get_ident_str(level) + cad
    
    def check_types(self,symbols):
        pass
    
    def execute(self,symbols):
        pass

class Program(Expre):
    
    def __init__(self, statement):
        Expre.__init__(self)
        self.type = "PROGRAM"
        self.statement = statement
        self.symbolTable = None
        
    def print_tree(self,level = 0):
        self.print_with_indent(self.type, level)
        self.statement.print_tree(level + 1)
    
    def check_types(self):
        self.symbolTable = SymbolTable()
        self.statement.check_types(self.symbolTable)
        
    def execute(self):
        self.symbolTable = SymbolTable()
        self.statement.execute(self.symbolTable)
        
class Scan(Expre):
    
    def __init__(self,id_):
        Expre.__init__(self)
        self.type = 'SCAN'
        self.var_to_read = id_
    
    def print_tree(self , level):
        self.print_with_indent(self.type,level)
        self.var_to_read.print_tree(level + 1)

    def check_types(self, symbolTable):
        type_var = self.var_to_read.check_types(symbolTable)
        if type_var == "": return ""
        
        if type_var not in ('int','bool'):
            static_errors.append((self.var_to_read.lineno,self.var_to_read.lexpos,
                                "'SCAN' solo se puede usar para variables de tipo 'int' o 'bool' . '%s' es de tipo '%s'" % \
                                    (self.var_to_read.name,type_var))
                                )
        
class Assign(Expre):
    
    def __init__(self, identifier, expression):
        Expre.__init__(self)
        self.type = "ASSIGN"
        self.id = identifier
        self.expression = expression
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.id.print_tree(level + 1)
        self.print_with_indent('value',level + 1)
        self.expression.print_tree(level + 2)
    
    #===========================================================================
    # def fetch_symbols(self, symbolTable):
    #     self.id.fetch_symbols(symbolTable)
    #     self.expression.fetch_symbols(symbolTable)
    # 
    #===========================================================================
    def check_types(self, symbolTable):
        self.id.check_types(symbolTable)
        symbol = symbolTable.lookup(self.id.name)
        if symbol is not None:
            type_expres = self.expression.check_types(symbolTable)
            
            if type_expres ==  "" : return ""

            if symbol.type != type_expres:
                static_errors.append((self.lineno,self.lexpos,
                                      "No se puede asignar expresiones de tipo '%s' a la variable '%s' de tipo '%s'." % (type_expres,self.id.name,symbol.type)))
            
            if "o" not in symbol.type_edit:
                static_errors.append((self.id.lineno,self.id.lexpos,
                                      "La variable %s es de solo lectura." % (self.id.name)))
                
    def execute(self, symbolTable):
        value = self.expression.evaluate(symbolTable)
        symbolTable.update(self.id.name, value)
                  
class If(Expre):
    
    def __init__(self,condition,statement_if, statement_else = None):
        Expre.__init__(self)
        self.type = 'IF'
        self.condition = condition
        self.statement_if   = statement_if
        self.statement_else = statement_else
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.print_with_indent("condition",level+1)
        self.condition.print_tree(level + 2)
        
        self.print_with_indent('THEN', level+1)
        self.statement_if.print_tree(level + 2)
        
        if self.statement_else is not None:
            self.print_with_indent('ELSE',level)
            self.statement_else.print_tree(level + 1)
            
        self.print_with_indent('END_IF',level)
    
        
    def check_types(self, symbolTable):        
        type_cond = self.condition.check_types(symbolTable)
 
        if  type_cond != "bool":
            if type_cond == "":
                static_errors.append((self.condition.lineno,self.condition.lexpos,
                                  "Instrucción 'if' espera expresiones de tipo 'bool'."))
            else:
                static_errors.append((self.condition.lineno,self.condition.lexpos,
                                  "Instrucción 'if' espera expresiones de tipo 'bool', no de tipo '%s'." % type_cond))
        
        self.statement_if.check_types(symbolTable)
        if self.statement_else is not None:
            self.statement_else.check_types(symbolTable)

class For(Expre):
    
    def __init__(self,identifier,direction, expression , statement):
        Expre.__init__(self)
        self.type = 'FOR'
        self.identifier = identifier
        self.direction  = direction
        self.expression = expression
        self.statement  = statement
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.identifier.print_tree(level + 1)
        self.direction.print_tree(level + 1)
        
        self.print_with_indent('IN',level + 1)
        self.expression.print_tree(level + 1)

        self.print_with_indent('DO',level + 1)
        self.statement.print_tree(level + 2)
        self.print_with_indent('END_FOR',level)
    
    def check_types(self, symbolTable):
        type_expre = self.expression.check_types(symbolTable)
        #self.identifier.check_types(symbolTable) # Esto hay que hacerlo??
        if type_expre != "set":
            if type_expre == "":
                static_errors.append((self.expression.lineno,self.expression.lexpos,"La expression de un for debe ser de tipo 'set'"))
            else:                          
                static_errors.append((self.expression.lineno,self.expression.lexpos,"La expression de un for debe ser de " +\
                                 "tipo 'set' no de tipo '%s'." % type_expre))
                
        symbolTable.add_scope() # Crea un nuevo alcance
        symbolTable.insert(self.identifier.name,"int","i") # Creacion simbolo de solo lectura
        self.statement.check_types(symbolTable)
        symbolTable.delete_scope() # Eliminar alcance saliendo del For
        
class RepeatWhileDo(Expre):
    
    def __init__(self,statement1,expression,statement2):
        Expre.__init__(self)
        self.type = 'REPEAT'
        self.statement1 = statement1
        self.expression  = expression
        self.statement2 = statement2
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.statement1.print_tree(level + 1)
        
        self.print_with_indent('WHILE',level)
        self.print_with_indent('condition',level + 1)
        self.expression.print_tree(level + 2)

        self.print_with_indent('DO',level)
        self.statement2.print_tree(level + 1)
      
    def check_types(self, symbolTable):
        self.statement1.check_types(symbolTable)
        
        type_expre = self.expression.check_types(symbolTable)
        if type_expre != "bool":
            if type_expre == "":
                static_errors.append((self.expression.lineno,self.expression.lexpos,"Condicion del 'while' debe ser de tipo 'bool'."))
            else:
                static_errors.append((self.expression.lineno,self.expression.lexpos,
                                  "Condicion del 'while' debe ser de tipo 'bool', no de tipo '%s'." % type_expre))
        
        self.statement2.check_types(symbolTable)
        
class WhileDo(Expre):
    
    def __init__(self,expression,statement):
        Expre.__init__(self)
        self.type = 'WHILE'
        self.expression  = expression
        self.statement = statement
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.print_with_indent('condition',level + 1)
        self.expression.print_tree(level + 2)

        self.print_with_indent('DO',level)
        self.statement.print_tree(level + 1)
        self.print_with_indent('END_WHILE',level)
    
    def check_types(self, symbolTable):
        type_expre = self.expression.check_types(symbolTable)
        if type_expre != "bool":
            if type_expre == "":
                static_errors.append((self.expression.lineno,self.expression.lexpos,"Condicion del 'while' debe ser de tipo 'bool'."))
            else:                          
                static_errors.append((self.expression.lineno,self.expression.lexpos,"Condicion del 'while' debe ser de" +\
                                 "tipo 'bool' no de tipo '%s'." % type_expre))
        
        self.statement.check_types(symbolTable)
    
class RepeatWhile(Expre):
    
    def __init__(self,statement,expression):
        Expre.__init__(self)
        self.type = 'REPEAT'
        self.statement = statement
        self.expression  = expression
        
    def print_tree(self,level): 
        self.print_with_indent(self.type,level)
        self.statement.print_tree(level + 1)

        self.print_with_indent('WHILE',level)
        self.print_with_indent('condition',level + 1)
        self.expression.print_tree(level + 2)

    def check_types(self, symbolTable):
        self.statement.check_types(symbolTable)
        type_expre = self.expression.check_types(symbolTable)
        if type_expre != "bool":
            if type_expre == "":
                static_errors.append((self.expression.lineno,self.expression.lexpos,"Condicion del 'while' debe ser de tipo 'bool'."))
            else:                          
                static_errors.append((self.expression.lineno,self.expression.lexpos,"Condicion del 'while' debe ser de" +\
                                 "tipo 'bool' no de tipo '%s'." % type_expre))       
    
class Print(Expre):
    
    def __init__(self,type_print,lista_to_print):
        Expre.__init__(self)
        self.type = type_print.upper()
        self.lista_to_print = lista_to_print
        
    def print_tree(self,level): 
        self.print_with_indent(self.type, level)
        for var in self.lista_to_print:
            var.print_tree(level + 1)
 
    def check_types(self, symbolTable):
        for exp in self.lista_to_print:
            exp.check_types(symbolTable)
            
        return self.type
    
    def execute(self, symbolTable):
        out = ""
        for exp in self.lista_to_print:
            out = out + str(exp.evaluate(symbolTable))
        print out
              
class Block(Expre):
    
    def __init__(self, list_st,declare = None): 
        Expre.__init__(self)
        self.type = "BLOCK"
        self.list_st = list_st
        self.declare = declare
        
    def print_tree(self,level):
        self.print_with_indent(self.type, level)
        
        if self.declare is not None:
            self.declare.print_tree(level + 1)

        for stat in self.list_st:
            stat.print_tree(level + 1)
            
        self.print_with_indent("BLOCK_END", level)
    
    def check_types(self, symbolTable):    
       
        if self.declare: # Vemos si el bloque tiene declaraciones
            symbolTable.add_scope() # Si el bloque tiene declaraciones, se agrega una nueva tabla
            self.declare.check_types(symbolTable)            
        
        for stat in self.list_st:
            stat.check_types(symbolTable)
        
        if self.declare: # Si hubo declaraciones, se desempila una tabla
            symbolTable.delete_scope()
    
    def execute(self, symbolTable):
        
        if self.declare: # Vemos si el bloque tiene declaraciones
            symbolTable.add_scope() # Si el bloque tiene declaraciones, se agrega una nueva tabla
            self.declare.execute(SymbolTable)            
        
        for stat in self.list_st:
            stat.execute(symbolTable)
        
        if self.declare: # Si hubo declaraciones, se desempila una tabla
            symbolTable.delete_scope()
            
class Parenthesis(Expre):
    
    def __init__(self, expre):
        Expre.__init__(self)
        self.type = 'PARENTHESIS'
        self.condition = expre   
            
    def print_tree(self,level):  
        self.print_with_indent(self.type , level)
        self.condition.print_tree(level + 1)
        self.print_with_indent('PARENTHESIS_CLOSE', level)
    
    def check_types(self, symbolTable):
        return self.condition.check_types(symbolTable)
    
class BinaryOP(Expre):
    bin_operators = {   
        # Int Operators
         "PLUS +"         : sum1,
         "MINUS -"        : minus,
         "TIMES *"        : times,
         "INTDIVISION /"  : int_division,
         "RESTDIVISION %" : rest_division,
         # Bool Operators
         "UNEQUAL /="        : unequal,
         "EQUALBOOL =="      : equal,
         "LESSTHAN <"        : less,
         "LESSOREQUALTHAN <=": less_equal,
         "GREATERTHAN >"     : greater,
         "GREATEROREQUALTHAN >=" : greater_equal,
         
         "and"    : binary_and,
         "or"     : binary_or,
         # Set Operators
         "UNION ++"        : union,
         "DIFFERENCE \\"   : difference,
         "INTERSECTION ><" : intersection,
         # int and set Operators
         "MAPPLUS <+>"     : map_plus,
         "MAPMINUS <->"    : map_minus,
         "MAPTIMES <*>"    : map_times, 
         "MAPDIVIDE </>"   : map_divide,
         "MAPREST <%>"     : map_rest,
         "BELONG @"        : belong
    }
    
    def __init__(self,expre1,type_op,expre2):
        Expre.__init__(self)
        self.expre1  = expre1
        self.type_op = type_op
        self.expre2  = expre2
        
    def print_tree(self,level):  
        self.print_with_indent(self.type_op, level)
        self.expre1.print_tree(level + 1)
        self.expre2.print_tree(level + 1)
            
    def check_types(self, symbols):
        #Check type for BinaryOP
        pass
    
    def evaluate(self, symbolTable):
        value1 = self.expre1.evaluate(symbolTable)
        value2 = self.expre2.evaluate(symbolTable)
        return BinaryOP.bin_operators[self.type_op](value1, value2)
    
class BinaryOpInteger(BinaryOP):
    ''' 
    Integer Binary Operator
    ("PLUS +","MINUS -","TIMES *","INTDIVISION /","RESTDIVISION %")
    '''
    def check_types(self,symbols):
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "int" and type_expre2 == "int"):
            static_errors.append((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-1],type_expre1,type_expre2)))
            return "" 
          
        return "int"
        
class BinaryOpEquals(BinaryOP):
    ''' Equals Binary Operator ("UNEQUAL /=","EQUALBOOL ==") '''
    def check_types(self,symbols):
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not ((type_expre1 == "bool" and type_expre2 == "bool") or \
                (type_expre1 == "set" and type_expre2 == "set")   or \
                (type_expre1 == "int" and type_expre2 == "int")) : 
            static_errors.append((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-2:],type_expre1,type_expre2)))
            return "" 
             
        return "bool"

class BinaryOpLessGreater(BinaryOP):
    '''
    Binary Compare Operator 
    ("LESSTHAN <","LESSOREQUALTHAN <=","GREATERTHAN >","GREATEROREQUALTHAN >=")
    '''
    def check_types(self,symbols):       
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "int" and type_expre2 == "int") : 
            static_errors.append((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-2:],type_expre1,type_expre2)))
            return "" 
            
        return "bool"
    
class BinaryOpBelong(BinaryOP):
    ''' Belong Binary Operator "BELONG @" '''
    def check_types(self,symbols):
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "int" and type_expre2 == "set") : 
            static_errors.append((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-1],type_expre1,type_expre2)))
            return "" 
             
        return "bool" 

class BinaryOpBool(BinaryOP):
    ''' "and" , "or" Binary boolean operator'''    
    def check_types(self,symbols):       
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "bool" and type_expre2 == "bool") :    
            static_errors.append((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op,type_expre1,type_expre2)))
            return ""
             
        return "bool"       

class BinaryOpSet(BinaryOP):
    ''' Set binary op ("UNION ++","DIFFERENCE \\","INTERSECTION ><")'''
    def check_types(self,symbols):       
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""

        if not (type_expre1 == "set" and type_expre2 == "set") : 
            static_errors.append((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-2:],type_expre1,type_expre2)))
            return "" 
             
        return "set"
    
class BinaryOpMapToSet(BinaryOP):
    '''
    Map to Set Binary Operator
    ("MAPPLUS <+>","MAPMINUS <->","MAPTIMES <*>","MAPDIVIDE </>","MAPREST <%>")
    '''
    def check_types(self,symbols):       
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "int" and type_expre2 == "set") : 
            static_errors.append((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-3:],type_expre1,type_expre2)))
            return "" 
             
        return "set" 
    
class UnaryOP(Expre):
    ''' Unary Operator for Inheritance'''
    unary_operators = {   
        "not"      : bool_not,   # Bool not
        "NEGATE -" : int_negate, # Integer negate
        #Unary set Operator 
        "MAXVALUESET >?" : max_value_set,
        "MINVALUESET <?" : min_value_set,
        "SIZESET $?"     : size_set,
    }
    def __init__(self, type_op,expre1):
        Expre.__init__(self)
        self.type_op = type_op
        self.expre1  = expre1
            
    def print_tree(self,level):   
        self.print_with_indent(self.type_op , level)
        self.expre1.print_tree(level + 1)
           
    def check_types(self, symbols):
        # For type checking
        pass
    
    def evaluate(self, symbolTable):
        value = self.expre1.evaluate(symbolTable)
        return UnaryOP.unary_operators[self.type_op](value)
        
class UnaryOpUminus(UnaryOP):
    def check_types(self, symbols):
        type_expre = self.expre1.check_types(symbols)
        if type_expre == "": return ""

        if type_expre != "int":
            static_errors.append((self.lineno,self.lexpos,"Operador unario '-' solo se puede aplicar a enteros" +\
                                 " no ha expresiones del tipo '%s'" % type_expre))
            return ""
        
        return "int"

class UnaryOpNot(UnaryOP):
    def check_types(self, symbols):
        type_expre = self.expre1.check_types(symbols)
        if type_expre == "": return ""
        
        if type_expre != "bool":
            static_errors.append((self.lineno,self.lexpos,"Operador unario 'not' solo se puede aplicar a expresiones booleanas" +\
                                 " no ha expresiones del tipo '%s'" % type_expre))
            return ""
          
        return "bool"

class UnaryOpSet(UnaryOP):
    ''' Unary set Operator ("MAXVALUESET >?","MINVALUESET <?","SIZESET $?")'''
    def check_types(self, symbols):
        type_expre = self.expre1.check_types(symbols)
        if type_expre == "": return ""
        
        if type_expre != "set":
            static_errors.append((self.lineno,self.lexpos,"Operador unario '%s' solo se puede aplicar a conjuntos" +\
                                 " no a expresiones del tipo '%s'" % (self.type_op[-2:],type_expre)))
            return ""
            
        return "int"
    
class DeclareList(Expre):
    
    def __init__(self,declared_list):
        Expre.__init__(self)
        self.declared_list = declared_list
        
    def print_tree(self,level):
        self.print_with_indent('USING', level)
        for declaration_vars in self.declared_list:
            declaration_vars.print_tree(level)
        self.print_with_indent('IN', level)
        
    def check_types(self, symbolTable):
        for declaration_vars in self.declared_list:
            declaration_vars.check_types(symbolTable)
            
    def execute(self, symbolTable):
        for declaration_vars in self.declared_list:
            declaration_vars.execute(symbolTable)
    
class TypeList(Expre):
    
    def __init__(self,data_type,id_list):
        Expre.__init__(self)
        self.data_type = data_type
        self.id_list = id_list
    
    def print_tree(self,level):
        for identifier in self.id_list:
            self.print_with_indent(self.data_type + ' ' + identifier.name,level + 1)
    
    def check_types(self, symbolTable):
        for var in self.id_list:
            
            if symbolTable.contains(var.name):
                symbol = symbolTable.lookup(var.name)
                static_errors.append((var.lineno,var.lexpos,
                                      "La variable '%s' ya ha sido declarada en este alcance " % (var.name) + \
                                      'en la linea %d, columna %d con tipo %s.' % (symbol.ref.lineno,\
                                                                                      obtener_columna_texto_lexpos(symbol.ref.lexpos),
                                                                                      symbol.type)))
            else:
                symbolTable.insert(var.name, self.data_type,'i/o',var)
        #return True
        
    def execute(self, symbolTable):
        for var in self.id_list:
            symbolTable.insert(var.name, self.data_type,'i/o',var)
            
class Direction(Expre):
    
    def __init__(self,value):
        Expre.__init__(self)
        self.type = 'direction'
        self.value = value
        
    def print_tree(self , level):
        self.print_with_indent(self.type, level)
        self.print_with_indent(self.value, level + 1)
        
    def check_types(self, symbolTable):
        return self.value

class Set(Expre):
    
    def __init__(self, list_st): 
        Expre.__init__(self)
        self.type = 'set'
        self.list_st = list_st
        
    def print_tree(self,level):
        self.print_with_indent(self.type, level)

        for exp in self.list_st:
            exp.print_tree(level + 1)
            
    def check_types(self, symbolTable):
        for exp in self.list_st:
            exp.check_types(symbolTable)
            
        return self.type
    
class Bool(Expre):
    
    def __init__(self , value):
        Expre.__init__(self)
        self.type = 'bool'
        self.value = value
    
    def print_tree(self , level):
        self.print_with_indent(self.type, level)
        self.print_with_indent(self.value, level + 1)

    def check_types(self, symbolTable):
        return self.type
    
    def evaluate(self, symbolTable):
        return self.value
    
class Integer(Expre):
    
    def __init__(self , value):
        Expre.__init__(self)
        self.type = 'int'
        self.value = value
        
    def print_tree(self , level):  
        self.print_with_indent(self.type, level)
        self.print_with_indent(str(self.value), level + 1)
        
    def check_types(self, symbolTable):
        return self.type
    
    def evaluate(self, symbolTable):
        return self.value
    
class String(Expre):
    
    def __init__(self , value):
        Expre.__init__(self)
        self.type = 'string'
        self.value = value
    
    def print_tree(self , level):  
        self.print_with_indent(self.type, level)
        self.print_with_indent(self.value, level + 1)
        
    def check_types(self, symbolTable):
        return self.type
    
    def evaluate(self, symbolTable):
        return self.value
    
class Identifier(Expre):
    
    def __init__(self , name):        
        Expre.__init__(self)
        self.name = name
        self.type = ""
        
    def print_tree(self , level):       
        self.print_with_indent("identifier"  , level )
        self.print_with_indent(self.name , level + 1 )
        
    def check_types(self, symbolTable):
        symbol = symbolTable.lookup(self.name)
        if symbol is None:
            static_errors.append((self.lineno,self.lexpos,"La variable '%s' aun no ha sido declarada."  % self.name))
        else:
            self.type = symbol.type
        return self.type
    
    def evaluate(self, symbolTable):
        symbol = symbolTable.lookup(self.name) 
        return symbol.value