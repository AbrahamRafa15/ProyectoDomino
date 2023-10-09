#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manual de usuario:
1. Como lo está especificado en las reglas, la mula más alta inicia 
(también hay casos en el que nadie tiene una mula, por lo tanto, se coloca cualquier ficha), 
así que hay que colocar los valores izquierdo y derecho, en ese orden. 
En la consola se van a imprimir ambos extremos, a manera de confirmación. 
Posteriormente pide confirmación para el turno, T (True) para indicar que es nuestro turno 
(es decir, el rival tiró la primera ficha), F (False) para el turno del rival 
(nosotros tiramos la primera ficha).

2. En este caso, nosotros tiramos primero, por lo que pregunta también si el rival comió 
(ya que es su turno): S, para indicar que si lo hizo; N, para indicar que no lo hizo
    a. Si el rival no comió, pedirá su movimiento (usando el principio de punto 2).
    b. Si el rival comió, hay que especificar cuántas, además de cuál fue el tiro que realizó.

3. “El otro extremo de la ficha que puso” y “Extremo del tablero donde puso la ficha”:
Al ingresar la ficha (o movimiento del rival [del paso anterior]), 
cada número va a ocupar una posición, el menor de los ingresados será el 0, y el mayor el 1 
Para indicarle como tiró el rival, le tenemos que indicar qué número de la ficha del rival quedó 
como extremo en el tablero (es lo que “El otro extremo de la ficha que puso” quiere decir), 
a partir del 0 o el 1.
“Extremo del tablero donde puso la ficha” se refiere a si jugó la pieza del lado izquierdo (ponemos 0), 
o el lado derecho (colocamos 1). 

Finalmente, imprimirá los nuevos extremos para confirmar y preguntará si seguiremos jugando, 
colocamos T para indicar que continuaremos y F para abandonar el juego.

4. Después del turno del rival, hay que señalar que jugamos nosotros, colocando una T. 
Nos indicará qué debemos hacer, ya sea comer o colocar una ficha
a. Si tenemos que colocar una ficha, nos indica cuál y en qué extremo, actualizándolos después.
b. Si tenemos que comer habrá que darle los valores de todas las fichas que vayamos comiendo 
hasta que haya una que podamos tirar.



"""
import numpy as np, copy

pozo = 14


def generaDiccionario():  # Genera el diccionario que vamos a utilizar para saber sobre las fichas
    diccionario_posibilidades = {}
    for i in range(7):  # Genera sólo las 28 fichas
        for j in range(i, 7):
            diccionario_posibilidades[(i, j)] = 1  # Inicializa en 1 porque existe esa ficha
    diccionario_posibilidades["rival"] = 7 #Para contar las fichas que tiene el diccionario
    return diccionario_posibilidades #Regresa las posibilidades del diccionario


class NodoDominó: #Clase dominó
    def __init__(self, mis_fichas, fichas_tab, turno, extremos, diccionario, movimiento=None): #Constructor
        
        self.fichas = mis_fichas #Fichas que tengo disponibles
        self.tablero = fichas_tab #Las fichas que se han jugado en el tablero
        self.turno = turno #El turno. True implica que somos nosotros, False implica el contrario
        self.extremos = extremos #Representa ambos extremos de la mesa. 0 representa la izquierda y 1 la derecha
        self.diccionario = diccionario #Tiene las fichas posibles que generamos en la función de arriba
        self.movimiento = movimiento #Tiene un objeto de tipo movimiento que representa cómo llegamos a ese estado
        self.hijos = [] #Contiene los hijos que tiene este nodo. Usualmente son las jugadas físicas o las diferentes que simulamos

    def generaMovimiento(self, movimiento):  # Generar un nuevo nodo hijo simulado con el movimiento
        
        nextremos = copy.deepcopy(self.extremos)  # Copiamos los extremos originales
        ntab = copy.deepcopy(self.tablero)  # Copiamos el tablero original
        f = movimiento.ficha  # Obtenemos el atributo ficha del movimiento
        diccionario_pos = copy.deepcopy(self.diccionario) #Hacemos una copia del diccionario que tiene las fichas disponibles
        diccionario_pos[f] = 0 #Actualizamos el diccionario para que refleje que se dio esa ficha
        
        if self.turno == True:  # Si nosotros estamos jugando
            nlista = copy.deepcopy(self.fichas)  # Hacemos una copia de nuestras fichas
            nlista.remove(movimiento.ficha)  # Retiramos la ficha que jugamos de nuestra lista de fichas
            ntab.append(f)  # Agregamos esa ficha al tablero nuevo
            nextremos[movimiento.extremot] = f[
                movimiento.extremof]  # actualizamos los extremos, movimiento.extremot representa el lado del tablero y movimiento.extremof representa el lado de la ficha que vamos a dejar libre
            nturno = not self.turno  # Cambiamos el turno porque le tocaría al contrincante
            hijo = NodoDominó(nlista, ntab, nturno, nextremos, diccionario_pos, movimiento) #Creamos un nuevo hijo que refleje ese movimiento simulado
            self.hijos.append(hijo) #Agregamos el hijo a la lista
            return hijo  # Regresamos el nodo hijo
        else:  # Si no
            diccionario_pos["rival"] -= 1 #Quitamos una ficha del rival en la simulación
            nextremos[movimiento.extremot] = f[
                movimiento.extremof]  # actualizamos los extremos, movimiento.extremot representa el lado del tablero y movimiento.extremof representa el lado de la ficha que vamos a dejar libre
            nturno = not self.turno  # Cambiamos el turno porque nos tocaría a nosotros
            hijo = NodoDominó(self.fichas, ntab, nturno, nextremos, diccionario_pos, movimiento) #Creamos un nuevo hijo que refleje el movimiento simulado
            self.hijos.append(hijo) #Agregamos el nodo hijo
            return hijo  # Regresamos el nodo hijo

    def juega(self, movimiento):  # Aquí vamos a jugar de manera real, por lo que vamos a modificar todo
        
        f = movimiento.ficha  # Obtenemos el atributo ficha del movimiento
        self.tablero.append(f)  # Agregamos esa ficha al tablero nuevo
        self.extremos[movimiento.extremot] = f[
            movimiento.extremof]  # actualizamos los extremos, movimiento.extremot representa el lado del tablero y movimiento.extremof representa el lado de la ficha que vamos a dejar libre
        self.diccionario[f] = 0 #Actualizamos la ficha que ya usamos (o us y sabemos que se jugó
        
        if self.turno == True:  # Si nosotros estamos jugando
            self.fichas.remove(movimiento.ficha)  # Retiramos la ficha que jugamos de nuestra lista de fichas
            nturno = not self.turno  # Cambiamos el turno porque le tocaría al contrincante
            hijo = NodoDominó(self.fichas, self.tablero, nturno, self.extremos, self.diccionario, movimiento)
            self.hijos.append(hijo)
            return hijo  # Regresamos el nodo hijo
        else:  # Si no, agregamos la que va a jugar
            self.diccionario["rival"] -= 1 #Disminuimos las fichas del rival
            nturno = not self.turno  # Cambiamos el turno porque nos tocaría a nosotros
            hijo = NodoDominó(self.fichas, self.tablero, nturno, self.extremos, self.diccionario, movimiento)
            self.hijos.append(hijo)
            return hijo  # Regresamos el nodo hijo


class Movimiento: #Clase movimiento

    def __init__(self, ficha, extremof, extremot, descripcion):
        
        self.ficha = ficha #Le asignamos la ficha que vamos a jugar
        self.extremof = extremof #El extremo contrario de la ficha. Por ejemplo, si jugamos (2,5) y ponemos el 2, entonces el valor será 1 porque representa el 5 que quedó libre
        self.extremot = extremot #Representa el extremo donde lo vamos a poner
        self.descripcion = descripcion #Nos dice qué vamos a hacer expresado en palabras

    def __str__(self):
        return self.descripcion


def generaFichas():  # Función para generar las fichas
    x = int(input("Dame el primer valor ")) #Primer valor de la ficha
    y = int(input("Dame el segundo valor ")) #Segundo valor de la ficha
    return (min(x, y), max(x,y))


def checaFicha(ficha, extremo, jugadas): #Checa las posibilidades con los 4 posibles combinaciones, cada extremo con las fichas
    if ficha[0] == extremo[
        0]:  # Si el extremo izquierdo de nuestra ficha coincide con el izquierdo del tablero, podemos jugar
        jugadas.append(
            Movimiento(ficha, 1, 0, "Ficha " + str(ficha) + ". Poner el " + str(ficha[0]) + " en el extremo izquierdo"))
    if ficha[1] == extremo[
        0]:  # Si el extremo derecho de nuestra ficha coincide con el izquierdo del tablero, podemos jugar
        jugadas.append(
            Movimiento(ficha, 0, 0, "Ficha " + str(ficha) + ". Poner el " + str(ficha[1]) + " en el extremo izquierdo"))
    if ficha[1] == extremo[
        1]:  # Si el extremo derecho de nuestra ficha coincide con el izquierdo del tablero, podemos jugar
        jugadas.append(
            Movimiento(ficha, 0, 1, "Ficha " + str(ficha) + ". Poner el " + str(ficha[1]) + " en el extremo derecho"))
    if ficha[0] == extremo[
        1]:  # Si el extremo izquierdo de nuestra ficha coincide con el derecho del tablero, podemos jugar
        jugadas.append(
            Movimiento(ficha, 1, 1, "Ficha " + str(ficha) + ". Poner el " + str(ficha[0]) + " en el extremo derecho"))
    return jugadas


def jugadasPosibles(nodo, bol=True):  # Función de suma importancia que nos permite conocer cómo podemos jugar
    jugadas = []  # Aquí vamos a almacenar todas las tuplas que representan los movimientos
    extremo = nodo.extremos  # Obtenemos los extremos, que son una lista [x,y], con x: izquierda y: derecha
    total = len(nodo.fichas)  # obtenemos el total de nuestras fichas
    if nodo.turno: #Si es nuestro turno vamos a checar nuestras fichas
        if bol: # Esta bandera nos permite saber si estamos checando todas las fichas o sólo la que acabamos de comer
            for i in range(total):  # Exploramos todas las fichas que tenemos
                ficha = nodo.fichas[i]  # para comodidad, creamos una variable ficha que almacene la que estamos viendo
                checaFicha(ficha, extremo, jugadas) #Llamamos a la función que calcula las combinaciones
        else: #Si tenemos que comer, sólo vemos el final
            ficha = nodo.fichas[-1] #Checamos la última
            checaFicha(ficha, extremo, jugadas) #Llamamos a la función que calcula las combinaciones

    else: #Si es del rival, checamos las posibilidades
        for ficha, valor in nodo.diccionario.items(): #Iteramos sobre todo el diccionario que no sea 0 (ya esté jugado)
            if valor == 1: #Si no se ha jugado, es desconocida
                checaFicha(ficha, extremo, jugadas) #Vemos las combinaciones

    return jugadas  # Regresa la lista con las tuplas de movimientos


def tengoMula(nodo): #Vemos si es una mula
    resp = False 
    ficha = nodo.movimiento.ficha #Sacamos la ficha
    if ficha[0] == ficha[1]: #Vemos que sean iguales
        return True
    return resp



def checaExtremos(nodo, nh):  # Función auxiliar para checar los extremos
    resp = False
    fichas = nh.fichas #Checamos las fichas de los hijos
    extremos = nodo.extremos #Vemos los extremos
    for ficha in fichas:
        if (ficha[0] == extremos[0] and ficha[1] == extremos[0]) or (
                ficha[1] == extremos[0] and ficha[1] == extremos[1]):  # Checamos que esté en los dos extremos
            return True
    return resp


def ambosExtremos(nodo):  # Checar si tenemos posibilidades de jugar en ambos extremos
    resp = False
    if len(nodo.hijos) > 0:  # Si tiene hijos
        for nh in nodo.hijos:  # Checamos si los hijos van a poder jugar si movemos al papá, esto es, haya posibilidad de jugar en ambos
            resp = checaExtremos(nodo, nh)  # Llamamos a la función auxiliar
    return resp

def tenemosMas(nodo): #Checar si tengo más de uno
    resp = False
    mayores = [0] * 7
    fm = nodo.movimiento.ficha #Ver la ficha del movimiento
    for ficha in nodo.fichas:
        mayores[ficha[0]] += 1 
        mayores[ficha[1]] += 1
    if max(mayores) in fm: #Si el mayor está en algún extremo, entonces priorizamos gastar
        return True
    return resp

def soloExtremo(nodo): #Si sólo ha jugado por un lado, entonces nos conviene tirar del otro
    resp = False
    cont = len(nodo.hijos)
    x = 0
    if cont > 0:
        for hijo in nodo.hijos:
            if hijo.extremo[0] == nodo.extremo[0] or hijo.extremo[1] == nodo.extremo[1]:
                x += 1
    if cont == x:
        return True
    return resp

"""
def fe():
    import random
    return random.randint(1, 5)
"""

def funcionHeuristica(nodo):
    if tengoMula(nodo):  # Si hay mula, es la prioridad
        return 8
    if ambosExtremos(nodo):  # Si logro que tener fichas para ambos extremos
        return 7
    if tenemosMas(nodo): #Si tengo muchas fichas de uno
        return 6
    if soloExtremo(nodo): #Si sólo tira de un lado
        return 5
    else:
        return 1


def checaCierre(diccionario, extremos):
    ans = False
    for clave in diccionario.keys():
        if clave[0] == extremos[0] or clave[0] == extremos[1] or clave[1] == extremos[1] or clave[1] == extremos[0]:
            if diccionario[clave] == 1:
                return True
    return ans


def estadoFinal(nodo):
    global fichas_posibilidades
    if len(nodo.fichas) == 0:  # Ya no tenemos fichas
        return True
    if pozo == 0:  # Ya no hay fichas para comer
        return True
    if not checaCierre(nodo.diccionario, nodo.extremos):  # Ya no hay más fichas para tirar, el juego está cerrado
        return True
    if nodo.diccionario["rival"] == 0:  # El contrario ya no tiene fichas
        return True

    return False


def nodosHijos(nodo, bol=True): #Generar los nodos hijos
    hijos = []
    if not estadoFinal(nodo): #Si no estamos en un estado final
        for movimiento in jugadasPosibles(nodo, bol): #Generamos los movimientos para cada jugada posible
            hijos.append(nodo.generaMovimiento(movimiento)) #Los agregamos a los hijos
    return hijos


def minimax(nodo, profundidad, jugador, alfa=-np.inf, beta=np.inf):  # Algoritmo minimax con poda alfa-beta
    if profundidad == 0 or estadoFinal(
            nodo):  # Si ya llegamos al máximo de profundidad o estamos en un estado inicial, regresamos el valor de la función heurística
        return funcionHeuristica(nodo)  # llamamos a la función heurística

    if jugador:  # Si el jugador somos nosotros == True, entonces queremos maximizar
        bestValue = -np.inf  # Declaramos el valor como -infinito ∞
        for child in nodosHijos(
                nodo):  # Exploramos los hijos que nos regresa la función nodosHijos mandando el estado inicial=nodo con el que empeza
            val = minimax(child, profundidad - 1, False, alfa,
                          beta)  # Llamada recursiva para obtener el valor heurístico de maximizar nuestra jugada
            bestValue = max(bestValue,
                            val)  # Checamos el máximo entre el mejor valor que teníamos y el nuevo que obtuvimos
            alfa = max(alfa, bestValue)  # Obtenemos el máximo entre alfa y el mejor valor
            if beta <= alfa:  # Si beta<= alfa significa que no le conviene explorar más los hijos del nodo porque el contrario no iría por ahí, por lo que nos salimos
                break
        return bestValue  # Regresamos el mejor valor
    else:
        bestValue = np.inf  # Es análogo al de arriba, sólo que queremos minimizar
        for child in nodosHijos(nodo):
            val = minimax(child, profundidad - 1, True, alfa, beta)
            bestValue = min(bestValue, val)
            beta = min(beta, bestValue)
            if beta <= alfa:  # Si beta <= alfa significa que no nos conviene a nosotros elegir por ahí, entonces no exploramos los nodos hijos y nos salimos
                break
        return bestValue


def obtenerMovimiento(nodo, profundidad, jugador, bol=True): #Función para obtener el nuevo movimiento
    mejor = -np.inf #Mejor como -infinito
    mejorMovimiento = None 

    for nodoHijo in nodosHijos(nodo, bol): #Checamos los hijos para el estado base
        if bol: #si no comemos
            valor = minimax(nodoHijo, profundidad - 1, jugador) #Obtenemos el valor minimax
            if valor > mejor: #Si el valor es mejor al anterior
                mejor = valor #cambiamos el valor
                mejorMovimiento = nodoHijo.movimiento #obtenemos el mejor movimiento
        else:
            mejorMovimiento = nodoHijo.movimiento #Mandamos el mejor movimiento del que comimos
    return mejorMovimiento


def actualizarJuego(nodo, movimiento): #Función para actualizar el juego
    return nodo.juega(movimiento) #Regresa el movimiento de jugar


def jugar(): #Función para jugar
    global pozo
    print("Vamos a jugar dominó\n") 
    print("Dame las fichas que necesito\n")
    fichas = [] #nuestras fichas
    tablero = [] #el tablero
    extremos = [-1, -1] #Los extremos que vamos a jugar
    fichas_posibilidades = generaDiccionario() #Generamos el diccionario con las 28 fichas
    for i in range(7): #Generamos nuestras primeras 7 fichas
        f = generaFichas() #Llama a la función que genera las fichas
        fichas.append(f) #Agregamos las fichas a mi lista
    print("\nEmpieza quien tenga mula o el que tenga la ficha más alta")
    extremos[0] = int(input("\nDame el número de la ficha del lado izquierdo ")) #Obtenemos el extremo izquierdo
    extremos[1] = int(input("Dame el número de la ficha del lado derecho ")) #Obtenemos el extremo derecho
    print("Extremos: " + str(extremos)) #Imprimimos los extremos

    if tuple(extremos) in fichas: #Si nosotros tiramos primero, entonces lo quitamos de nuestras fichas
        fichas.remove(tuple(extremos))
        
    fichas_posibilidades[tuple(extremos)] = 0 #Actualizamos el diccionario porque ya usamos la ficha

    turno = (input("\n¿Quién escoge? T/F "))
    if turno == "T": #Si nos toca, entonces el turno ees True
        turno = True
    else:
        turno = False

    tablero.append(tuple(extremos)) #Agregamos al tablero la ficha que pusimos

    nodo = NodoDominó(fichas, tablero, turno, extremos, fichas_posibilidades) #Creamos el estado inicial

    bandera = True

    while bandera:
        if turno: #si tiramos
            mov = obtenerMovimiento(nodo, 3, turno) #Obtenemos el movimiento
            while mov is None and pozo > 0: #Mientras no tengamos para jugar, comemos; además, checar si hay para comer
                print("Hay que comer") 
                f = generaFichas() #Generas una nueva ficha
                nodo.fichas.append(f) #Agregamos la ficha
                fichas_posibilidades[f] = 0 #Actualizamos las posibilidades porque ya salió esa ficha y la conocemos
                pozo -= 1 #Quitamos una del pozo
                mov = obtenerMovimiento(nodo, 3, turno, False) #Vemos si tenemos un movimiento válido con esa ficha
            print(mov) #Imprimimos el movimiento cuando tengamos
            nodo.turno = True #El turno es true
        else:
            r = input("¿Comió el rival S/N ") #Nos pregunta si comió el rival
            if r == 'S': #Si sí comió
                comió = int(input("¿Cuántas comió? ")) #Nos pregunta cuántas comió
                fichas_posibilidades["rival"] += comió #Sumamos cuántas comió
                pozo -= comió #Restamos al pozo las que comió
            print("Dame el movimiento del rival") 
            f = generaFichas() #Generamos la ficha que comió el rival
            extremof = int(input("El otro extremo de la ficha que puso ")) #Obtenemos el extremo contrario al que puso 
            extremot = int(input("Extremo del tablero donde puso la ficha ")) #Extremo donde puso la ficha 0=izquierda 1=derecha
            mov = Movimiento(f, extremof, extremot,
                             "Ficha " + str(f) + ". Poner el " + str(f[0]) + " en el extremo derecho") #Generamos un movimiento con lo que hizo el rival
            nodo.turno = False #El turno es false
        nodo = actualizarJuego(nodo, mov) #Actualizamos el juego
        if len(nodo.fichas) == 0: #Si tenemos 0 fichas, ganamos
            print("Ganaste")
            break
        elif nodo.diccionario["rival"] == 0: #Si el rival no tiene fichas, ganó
            print("Ganó el rival")
            break
        print("Extremos: " + str(nodo.extremos)) #Imprimimos cómo están los extremos
        y = input("¿Quieres seguir jugando? T/F ") #Pregunta si queremos seguir jugando
        if y == "T":
            x = input("\n¿Quién escoge? T/F ") #Nos pregunta a quién le toca. T=nosotros, F=contrincante
            if x == "F":
                turno = False
                nodo.turno = turno
            else:
                turno = True
                nodo.turno = turno
        else:
            bandera = False


jugar() #Llamamos a la función para jugar


