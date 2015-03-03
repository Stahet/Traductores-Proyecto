'''
Created on Mar 3, 2015

Funciones para el interpretador
@author: Jonnathan Ng
         Manuel Gonzalez
'''

# Unary bool Operator
def bool_not(bool1):
    return not bool1

def int_negate(int1):
    return (-1)*int1

# Unary set Operator 
def max_value_set(set1):
    return max(set1)

def min_value_set(set1):
    return min(set1)
def size_set(set1):
    return len(set1)

# Binary set Operator
def sum1(int1, int2):
    return int1 + int2

def minus(int1, int2):
    return int1 - int2

def times(int1, int2):
    return int1 * int2

def int_division(int1, int2):
    return int1 / int2

def rest_division(int1, int2):
    return int1 % int2

# Bool Operators
def unequal(bool1, bool2):
    return bool1 != bool2

def equal(bool1, bool2):
    return bool1 == bool2

def less(bool1, bool2):
    return bool1 < bool2

def less_equal(bool1, bool2):
    return bool1 <= bool2

def greater(bool1, bool2):
    return bool1 > bool2

def greater_equal(bool1, bool2):
    return bool1 >= bool2

def binary_and(bool1, bool2):
    return bool1 and bool2

def binary_or(bool1, bool2):
    return bool1 or bool2
         
# Set Operators
def union(set1, set2):
    return set1 | set2

def difference(set1, set2):
    return set1 - set2

def intersection(set1, set2):
    return set1 & set2

# Int and Set Operators    
def map_plus(int1, set1):
    return {int1+x for x in set1}

def map_minus(int1, set1):
    return {int1-x for x in set1}

def map_times(int1, set1):
    return {int1*x for x in set1}

def map_divide(int1, set1):
    return {int1/x for x in set1}

def map_rest(int1, set1):
    return {int1%x for x in set1}

def belong(int1, set1):
    return (int1 in set1)