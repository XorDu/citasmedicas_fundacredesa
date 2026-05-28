import os
import sys

print("Iniciando la configuración de la base de datos de Fundacredesa...")

# Ejecutamos el archivo seed.py que contiene toda la lógica de creación de DB y usuarios
try:
    with open('seed.py', 'r', encoding='utf-8') as f:
        code = f.read()
        exec(code)
    print("\n¡Base de datos inicializada correctamente!")
    print("Ya puedes cerrar esta ventana y ejecutar start.bat")
except Exception as e:
    print(f"\nOcurrió un error al inicializar la base de datos: {e}")

input("\nPresiona ENTER para salir...")
