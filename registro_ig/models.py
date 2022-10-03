import csv
import os
import sqlite3
from config import ORIGIN_DATA

def filas_to_diccionario(filas,columnas):
    resultado = []
    for fila in filas:
        posicion_columna = 0
        d = {}
        for campo in columnas:
            d[campo[0]] = fila[posicion_columna]
            posicion_columna += 1
        resultado.append(d)
    return resultado

def select_all():
    """
    Devolverá una lista con todos los registros (lista vacía) del fichero sqlite Movements.sqlite
    """
    con = sqlite3.connect(ORIGIN_DATA) #Conecta el SQL con Python
    cur = con.cursor() #Maneja los accesos al programa

    cur.execute("SELECT id, date, description, quantity from movements order by date;") #Ejecuta la query del select

    resultado = filas_to_diccionario(cur.fetchall(), cur.description)
    
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

def select_by(id):
    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()

    cur.execute("SELECT id, date, description, quantity from movements WHERE id = ?", (id,))

    resultado = filas_to_diccionario(cur.fetchall(), cur.description)

    con.close()

    if resultado:
        return resultado[0]
    return {}
    
      
def insert(registro):
    """
    INSERT INTO Movements (date, concept, quantity, values (?, ?, ?)),params (parametros)
    
    cur.execute("INSERT INTO Movements (date, concept, quantity, values (?, ?, ?)", ['2022-04-08', 'Cumple', -80])

    con.commit() #Muy importante
    
    antes de con.close(), hay que hacer un con.commit()
    """
    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    cur.execute("INSERT INTO movements(date,description,quantity) values(?,?,?)", registro)

    con.commit() #Sirve para guardar los datos en el SQLite3. Sin este paso, no se añade ninguna línea a index.html --- Asegura la integridad de los datos
    con.close()

def delete_by(id):
    con = sqlite3.connect(ORIGIN_DATA) #Conecta el SQL con Python
    cur = con.cursor() #Maneja los accesos al programa

    cur.execute("DELETE FROM movements WHERE id = ?", (id,)) #Ejecuta la query del select

    con.commit()
    con.close()