'''
Created on 2/2/2015

@author: manuggz
'''


    

def parsear(entrada):
    producciones = {'S':('S+S','1')}
    alfabeto = '1+'

    def esTerminal(a):
        return a in alfabeto
    
    def buscarInicialesDerivacion(terminal,producciones):
        iniciales = []
        finales = []
        for pro in producciones:
            if pro[0] == terminal:
                iniciales.append(pro)
            else:
                finales.append(pro)
                
        return iniciales + finales

    if not isinstance(entrada, str):
        raise TypeError('Error:"a" must be a String')
    
    if not entrada:
        raise ValueError('"entrada" must be not empty')
    
    for i in entrada:
        if not i in alfabeto:
            raise ValueError('"' + i +'"'+ ' is not in alphabet!')
            
    
    if not esTerminal(entrada[0]):
        raise ValueError(entrada[0] + 'must be a terminal')
    
    iniciales = buscarInicialesDerivacion(entrada[0],producciones['S'])
        
    print(entrada,iniciales)
    
    def contarTerminales(lista_texto):
        j = 0
        for i in lista_texto:
            if esTerminal(i): j += 1
        
        return j
    
    def derivarIzquierda(lista_texto,orden_producion):
        
        #Buscamos el primer no terminal
        i = 0
        tam_texto = len(lista_texto)
        if tam_texto > len(entrada): return ''.join(lista_texto)

        while i != tam_texto and esTerminal(lista_texto[i]): i += 1
        
        if i >= tam_texto: return ''.join(lista_texto)
        
        for reemplazo in producciones[lista_texto[i]]:
            posible = lista_texto[:i] + list(reemplazo) + lista_texto[i+1:]
            orden_producion.append(reemplazo)
            if derivarIzquierda(posible,orden_producion) != entrada:
                orden_producion.pop()
            else:
                return entrada
                

    orden = []
    for semilla in iniciales:
        orden.append(semilla)
        if derivarIzquierda(list(semilla),orden) == entrada:
            print 'Orden:',orden
            break
        else:
            orden.pop()
    
    
        

parsear('1+1+1')
    