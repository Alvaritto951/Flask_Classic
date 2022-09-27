import csv
import os
import sqlite3
from config import ORIGIN_DATA

def select_all():
    """
    Devolverá una lista con todos los registros (lista vacía) del fichero sqlite Movements.sqlite
    """
    con = sqlite3.connect(ORIGIN_DATA) #Conecta el SQL con Python
    cur = con.cursor() #Maneja los accesos al programa

    result = cur.execute("SELECT id, date, description, quantity from movements order by date;") #Ejecuta la query del select

    filas = result.fetchall() #Devuelve una lista de tuplas
    columnas = result.description #Archivo de solo lectura. Viene de la documentación de SQL
    #Mezclar filas y columnas para obtener lista de diccionarios --- Ver vídeo clase 27/09/2022
    resultado = []
    for fila in filas:
        posicion_columna = 0
        d = {}
        for campo in columnas:
            d[campo[0]] = fila[posicion_columna]
            posicion_columna += 1
        resultado.append(d)
    
    """
    Otra forma:
    resultado = []
    for fila in filas:
        d = {}
        for posicion, campo in enumerate(columnas):
            d[campo[0]] = fila[posicion]
        resultado.append(d)
    """
    con.close()

    return resultado #return result.fetchall() #Devuélveme todo (+ igual que fichero.close())


def insert(registro):
    """
    INSERT INTO Movements (dat, concept, quantity, values (?, ?, ?))

    parametros cur.execute("INSERT INTO Movements (dat, concept, quantity, values (?, ?, ?)", ['2022-04-08', 'Cumple', -80])

    antes de con.close(), hay que hacer un con.commit()
    """    