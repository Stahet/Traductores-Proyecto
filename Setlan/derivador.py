'''
Creado el dia 27/1/2015

@author: Manuel Gonzalez   11-10390
@author: Jonnathan Ng 11-10199

Grupo 13

'''


def esTerminal(a , alfabeto):
    return a in alfabeto

def contarTerminales(lista_texto):
    j = 0
    for i in lista_texto:
        if esTerminal(i): j += 1
    
    return j

def derivarIzquierda(lista_texto,orden_producion,entrada,producciones,alfabeto):
    'Deriva un texto por la izquierda'
    i = 0
    tam_texto = len(lista_texto)
    if tam_texto > len(entrada): return -1 #Si el texto pasado a derivar tiene mas caracteres que el buscado
    #Buscamos el primer no terminal por la izquierda
    while i != tam_texto and esTerminal(lista_texto[i],alfabeto): i += 1
    
    if i >= tam_texto: return ''.join(lista_texto) #Si todos son no terminales regresamos el texto
    
    for id_reemplazo in range(len(producciones[lista_texto[i]])):
        #posible = texto a derivar con el no terminal reemplazado por una regla
        aprobado = True
        
        for j in producciones[lista_texto[i]][id_reemplazo]:
            if esTerminal(j, alfabeto) and j not in entrada:
                aprobado = False
                break
        
        if esTerminal(producciones[lista_texto[i]][id_reemplazo], alfabeto) and\
            tam_texto != len(entrada):
            aprobado = False
            
        if esTerminal(producciones[lista_texto[i]][id_reemplazo], alfabeto) and\
            producciones[lista_texto[i]][id_reemplazo] != entrada[i]:
            aprobado = False
            
        if aprobado:
            posible = lista_texto[:i] + list(producciones[lista_texto[i]][id_reemplazo]) + lista_texto[i+1:] 
            orden_producion.append((producciones[lista_texto[i]][id_reemplazo],id_reemplazo))
            if derivarIzquierda(posible,orden_producion,entrada,producciones,alfabeto) != entrada:
                orden_producion.pop()
            else:
                return entrada

def parsear(entrada):
    'Dada una gramatica deriva entrada por la izquierda'
    producciones = {'S':('x','y','z','S+S','S-S','S*S','S/S','(S)')}
    alfabeto = 'xyz+-*/()'

    if not isinstance(entrada, str):
        raise TypeError('Error:"a" must be a String')
    
    if not entrada:
        raise ValueError('"entrada" must be not empty')
    
    for i in entrada:
        if not i in alfabeto:
            raise ValueError('"' + i +'"'+ ' is not in alphabet!')
            
    
    if not esTerminal(entrada[0],alfabeto):
        raise ValueError(entrada[0] + 'must be a terminal')
    
    orden = []
    if derivarIzquierda(list('S'),orden,entrada,producciones,alfabeto) == entrada:
        print 'Orden:',orden    
        

parsear('(x+y)*x-y*(z)') 
parsear('(x+y)') 
