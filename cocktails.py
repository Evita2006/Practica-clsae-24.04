import requests
import sqlite3
import time

# 1. Obtener lista de cócteles
def obtener_cocteles():
    url = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Cocktail'
    respuesta = requests.get(url)
    datos = respuesta.json()
    return datos['drinks']

# Crear conexión a la base de datos y tabla
conexion = sqlite3.connect('cocktails.db')
cursos = conexion.cursor()
cursos.execute('''
    CREATE TABLE IF NOT EXISTS cocktails (
        idDrink TEXT PRIMARY KEY,
        strDrink TEXT,
        strCategory TEXT,
        strAlcoholic TEXT,
        strGlass TEXT
    )
''')
conexion.commit()

# Guardar datos en la base de datos
def guardar_en_bd(cocteles):
    conexion = sqlite3.connect('cocktails.db')
    cursor = conexion.cursor()
    for c in cocteles:
        cursor.execute('''
            INSERT OR REPLACE INTO cocktails (idDrink, strDrink)
            VALUES (?, ?)
        ''', (c['idDrink'], c['strDrink']))
    conexion.commit()
    conexion.close()

# Leer datos desde la base de datos
def leer_desde_bd():
    conexion = sqlite3.connect('cocktails.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM cocktails')
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

# Modificar un cóctel en la base de datos
def modificar_coctel():
    id_cambiar = input("Introduce el ID del cóctel que quieres modificar: ")
    nuevo_nombre = input("Nuevo nombre del cóctel: ")
    conexion = sqlite3.connect('cocktails.db')
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE cocktails SET strDrink = ? WHERE idDrink = ?
    ''', (nuevo_nombre, id_cambiar))
    conexion.commit()
    conexion.close()
    print("¡Cóctel actualizado!\n")

# Comparar tiempos entre API y base de datos
def comparar_tiempos():
    print("Comparando eficiencia temporal...")

    # Tiempo desde la API
    inicio_api = time.time()
    cocteles_api = obtener_cocteles()
    for c in cocteles_api:
        _ = c['strDrink']
    fin_api = time.time()
    tiempo_api = fin_api - inicio_api

    # Tiempo desde la base de datos
    inicio_bd = time.time()
    cocteles_bd = leer_desde_bd()
    for c in cocteles_bd:
        _ = c[1]  # strDrink
    fin_bd = time.time()
    tiempo_bd = fin_bd - inicio_bd

    print(f"\n Tiempo API: {tiempo_api:.4f} segundos")
    print(f" Tiempo BD:  {tiempo_bd:.4f} segundos")

    if tiempo_api > tiempo_bd:
        print(" Leer desde la base de datos es más rápido.")
    else:
        print(" Leer desde la API fue más rápido (posible caché de red o pocos datos).")

# Programa principal
def main():
    cocteles = obtener_cocteles()
    guardar_en_bd(cocteles)

    print("\n Cócteles guardados en la base de datos:")
    for idDrink, strDrink, _, _, _ in leer_desde_bd():
        print(f"{idDrink} - {strDrink}")

    modificar_coctel()

    print("Datos después de la modificación:")
    for idDrink, strDrink, _, _, _ in leer_desde_bd():
        print(f"{idDrink} - {strDrink}")

    comparar_tiempos()

if __name__ == '__main__':
    main()