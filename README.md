# Supercontrolador MySQL

## Descripción

Este es un proyecto de ejemplo que crea una interfaz gráfica (GUI) usando Tkinter para manejar bases de datos MySQL. Puedes ver las tablas, insertar nuevos registros y eliminar registros existentes de manera sencilla.

## Características

- **Interfaz gráfica fácil de usar**: Utiliza Tkinter y ttkbootstrap para un diseño moderno.
- **Gestión dinámica**: Detecta automáticamente las tablas y columnas de tu base de datos.
- **Operaciones básicas**: Inserta y elimina registros con facilidad.

## Requisitos

- Python 3.x
- Librerías:
  - `tkinter`
  - `ttkbootstrap`
  - `mysql-connector-python`

## Instalación

1. Clona este repositorio o descarga los archivos.
   
3. Instala las librerías necesarias:
   
   pip install mysql-connector-python ttkbootstrap
  
5. Configuración de la base de datos
   
   Busca la sección de configuración de la base de datos (DB_CONFIG):

   DB_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'database': 'tu_base_de_datos'
   }

   Cambia los valores según tu configuración:
   
    host: El host de tu base de datos MySQL (por ejemplo, localhost).
    user: Tu nombre de usuario de MySQL.
    password: Tu contraseña de MySQL.
    database: El nombre de la base de datos que quieres usar.


   

