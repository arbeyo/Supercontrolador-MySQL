import tkinter as tk         # Biblioteca estándar para interfaces gráficas
from tkinter import ttk       # Biblioteca para widgets mejorados
from ttkbootstrap import Style # Biblioteca para estilos modernos en ttk
import mysql.connector        # Conector para bases de datos MySQL

# Configuración de conexión a la base de datos (MODIFICAR AQUÍ)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'database': 'tu_base_de_datos'
}

# Variables globales para gestionar el estado
listacampos = []            # Lista de widgets del formulario de inserción
tablaactual = ''            # Tabla seleccionada actualmente
identificador_seleccionado = 0  # Identificador del registro seleccionado
campo_id = ''               # Nombre del campo de clave primaria

def conecta_base_datos(config):
    """
    Establece la conexión a la base de datos usando la configuración proporcionada.
    """
    return mysql.connector.connect(**config)

# Conexión a la base de datos usando la configuración proporcionada (MODIFICAR AQUÍ)
conexion = conecta_base_datos(DB_CONFIG)
cursor = conexion.cursor()

def eliminaRegistro():
    """
    Elimina el registro seleccionado en la tabla actual.
    """
    print("Voy a eliminar el registro que está seleccionado")
    print("La tabla seleccionada es: " + tablaactual)
    print("El identificador seleccionado es: " + str(identificador_seleccionado))
    # Construcción de la consulta SQL para eliminar el registro
    peticion = f"DELETE FROM {tablaactual} WHERE {campo_id} = {identificador_seleccionado};"
    print(peticion)
    cursor.execute(peticion)   # Ejecuta la consulta SQL
    conexion.commit()          # Confirma los cambios en la base de datos
    seleccionaTabla(tablaactual)  # Actualiza la vista de la tabla

def clickEnArbol(event):
    """
    Maneja el evento de clic en el árbol para seleccionar un registro.
    """
    global identificador_seleccionado
    print("Has hecho click en el árbol")
    elemento = arbol.identify('item', event.x, event.y)  # Identifica el ítem seleccionado
    arbol.selection_set(elemento)  # Marca el ítem como seleccionado
    valores = arbol.item(elemento, 'values')  # Obtiene los valores del registro seleccionado
    print(valores)
    identificador_seleccionado = valores[0]  # Actualiza la variable global con el identificador

def insertaBaseDatos():
    """
    Inserta un nuevo registro en la base de datos utilizando los valores ingresados en el formulario.
    """
    print("Insertamos en la base de datos")
    print(listacampos)
    # Construye la consulta SQL para insertar el nuevo registro
    peticion = f"INSERT INTO {tablaactual} VALUES (NULL,"

    for campo in range(1, len(listacampos)):
        peticion += f"'{listacampos[campo].get()}',"
    peticion = peticion[:-1]  # Elimina la última coma
    peticion += ")"           # Cierra la consulta
    print(peticion)
    cursor.execute(peticion)  # Ejecuta la consulta
    conexion.commit()         # Confirma los cambios en la base de datos
    seleccionaTabla(tablaactual)  # Actualiza la vista de la tabla

def seleccionaTabla(mitabla):
    """
    Actualiza la interfaz gráfica para reflejar los campos y registros de la tabla seleccionada.
    """
    global listacampos
    global tablaactual
    global campo_id
    tablaactual = mitabla
    print("Has pulsado la tabla de: " + mitabla)
    for widget in contieneformulario.winfo_children():
        widget.destroy()  # Limpia todos los widgets del formulario de inserción
    cursor.execute(f"SHOW COLUMNS IN {mitabla}")  # Obtiene las columnas de la tabla
    columnas = cursor.fetchall()
    listacampos = []  # Limpia la lista de campos
    # Encuentra el campo de clave primaria
    for columna in columnas:
        if columna[3] == 'PRI':
            campo_id = columna[0]
        ttk.Label(contieneformulario, text=columna[0]).pack(padx=5, pady=5)
        listacampos.append(ttk.Entry(contieneformulario))
        listacampos[-1].pack(padx=5, pady=5)
    ttk.Button(contieneformulario, text="Insertar", command=insertaBaseDatos).pack(padx=5, pady=5)
    # Limpia el árbol (tabla visual) de registros previos
    for elemento in arbol.get_children():
        arbol.delete(elemento)
    for columna in arbol['columns']:
        arbol.column(columna, width=0)
        arbol.heading(columna, text='')
    # Rellena el árbol con los datos de la tabla seleccionada
    listadocolumnas = [columna[0] for columna in columnas]
    print(tuple(listadocolumnas))
    arbol['columns'] = tuple(listadocolumnas)
    for unacolumna in listadocolumnas:
        arbol.heading(unacolumna, text=unacolumna)
        arbol.column(unacolumna, width=100)
    cursor.execute(f"SELECT * FROM {mitabla}")  # Selecciona todos los registros de la tabla
    registros = cursor.fetchall()
    for registro in registros:
        arbol.insert('', 'end', values=registro)  # Inserta cada registro en el árbol

# Configuración de la interfaz gráfica principal
raiz = tk.Tk()
Style(theme='cosmo')  # Aplica un tema moderno
raiz.geometry("800x400")  # Define el tamaño de la ventana
raiz.columnconfigure(0, minsize=100)
raiz.columnconfigure(1, minsize=100)
raiz.columnconfigure(2, minsize=600)
raiz.rowconfigure(0, weight=1)

# Sección para contener los botones de tablas
contienetablas = ttk.LabelFrame(
    raiz,
    text="Tablas en la BBDD",
    borderwidth=1,
    width=100,
    relief="ridge"
)
contienetablas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
cursor.execute(f"SHOW TABLES IN {DB_CONFIG['database']}")
tablas = cursor.fetchall()
# Crea un botón para cada tabla en la base de datos
for tabla in tablas:
    ttk.Button(contienetablas, text=tabla[0], width=10, command=lambda tabla=tabla[0]: seleccionaTabla(tabla)).pack(padx=10, pady=10)

# Sección para el formulario de inserción
contieneformulario = ttk.LabelFrame(
    raiz,
    text="Formulario de inserción",
    borderwidth=1,
    width=100,
    relief="ridge"
)
contieneformulario.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Sección para mostrar los datos en el árbol
contienedatos = ttk.LabelFrame(
    raiz,
    text="Datos en mi sistema",
    borderwidth=1,
    width=600,
    relief="ridge"
)
contienedatos.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
arbol = ttk.Treeview(contienedatos)
arbol.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Vincula el evento de clic en el árbol para seleccionar un registro
arbol.bind('<Button-1>', clickEnArbol)

# Botón para eliminar el registro seleccionado
ttk.Button(contienedatos, text="Elimina el registro seleccionado", command=eliminaRegistro).grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# Ejecuta el bucle principal de la interfaz gráfica
raiz.mainloop()
