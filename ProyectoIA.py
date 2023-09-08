#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 17:36:49 2023

@author: abrahammartinezceron
"""
import random

def actualizarRival(rival, tupla):
    if tupla not in rival:
        rival.append(tupla)
    
def actualizarYo(fichas, tupla):
    if tupla not in fichas:
        fichas.append(tupla)
  
    
def generaTuplas():
    return (random.randint(0, 6), random.randint(0, 6))

def actualizaDiccionario(diccionario, ficha, valor):
    if valor == 0:
        diccionario[ficha] = valor
    else:
        diccionario[ficha] = valor
    
    

def generaDiccionario():
    d = {}
    for i in range(7):
        for j in range(7):
            d[(i,j)] = 2
    return d
            


"""
Prueba
"""

rival = []
fichas = []
ficha1 = generaTuplas()
d = generaDiccionario()
print("Ejemplo de una ficha")
print(ficha1)
for i in range(7):
    f = generaTuplas()
    actualizarRival(rival, f)
print("Las fichas del rival son")
print(rival)
#print("")
#print(generaDiccionario())
for i in range(7):
    f = generaTuplas()
    actualizarYo(fichas, f)
    actualizaDiccionario(d, f, 0)

print("Mis fichas")
print(fichas)