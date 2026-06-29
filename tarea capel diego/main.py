import sqlite3 #Importamos la libreria Sqlite
import tkinter as tk #Importamos la libreria Sqlite

conexion = sqlite3.connect("tareas.db") #Conectamos Sqlite al archivo q nosotros queramos que se guarden los datos. este archivo se crea automaticamente

cursor = conexion.cursor() #el cursor es donde nosotros podemos realizar todas las consultas con la base sql

#en esta parte hemos investigado del lenguaje sqlite
cursor.execute("""
CREATE TABLE IF NOT EXISTS tareas(
    id_numeros INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    realizada INTEGER DEFAULT 0
)
""")

#Creamos el id_numeros para que sea nuestra primary key autoincrementable. ese integer no es nada raro, es int 
#Creamos otra columna q se llama descripcion de tipo texto y no nula 
#la columna realizada la creamos para dejar evidencia en la completación de nuestras tareas
#Realizada es otra variable entera

conexion.commit() #Esto es lo que vimos en las clases de GitHub. Un commit sirve para guardar cambios

#Funciones declaradas para que todos nuestros botones anden. Esta parte fue la que mas nos costo entender. Usamos IA pero intentamos entender el código

def cargar_tareas():
    lista.delete(0, tk.END)
    cursor.execute("SELECT descripcion, realizada FROM tareas")
    tareas = cursor.fetchall()

    for tarea in tareas:
        texto = tarea[0]

        if tarea[1] == 1: 
            texto = texto + " ✔"

        lista.insert(tk.END, texto)


def agregar_tarea():
    tarea = entrada.get()

    if tarea != "":
        cursor.execute(
            "INSERT INTO tareas(descripcion) VALUES (?)",
            (tarea,)
        )
        conexion.commit()

        entrada.delete(0, tk.END)
        cargar_tareas()


def eliminar_tarea():
    seleccion = lista.curselection()

    if seleccion:
        tarea = lista.get(seleccion[0])
        tarea = tarea.replace(" ✔", "")

        cursor.execute(
            "DELETE FROM tareas WHERE descripcion = ?",
            (tarea,)
        )
        conexion.commit()

        cargar_tareas()


def marcar_realizada():
    seleccion = lista.curselection()

    if seleccion:
        tarea = lista.get(seleccion[0])

        tarea = tarea.replace(" ✔", "")

        cursor.execute(
            "UPDATE tareas SET realizada = 1 WHERE descripcion = ?",
            (tarea,)
        )
        conexion.commit()

        cargar_tareas()


#Todo este choclazo es el diseño con la libreria tkinter (Gracias Felipe). No es tal vez el más bonito, pero si el más funcional.

ventana = tk.Tk()

ventana.title("Lista de Tareas")
ventana.geometry("500x450")
ventana.resizable(False, False)

#Titulo
titulo = tk.Label(
    ventana,
    text="LISTA DE TAREAS",
    font=("Arial",18,"bold")
)

titulo.pack(pady=15)

#Etiqueta
descripcion = tk.Label(
    ventana,
    text="Descripción:"
)

descripcion.pack()

#Caja de texto
entrada = tk.Entry(
    ventana,
    width=40
)

entrada.pack(pady=5)

#Botón agregar
boton_agregar = tk.Button(
    ventana,
    text="Agregar tarea",
    command=agregar_tarea
)

boton_agregar.pack(pady=10)

#Lista donde aparecerán las tareas
lista = tk.Listbox(
    ventana,
    width=50,
    height=10
)

lista.pack(pady=10)

#Botón marcar realizada
boton_realizada = tk.Button(
    ventana,
    text="Marcar realizada",
    command=marcar_realizada
)

boton_realizada.pack(pady=5)

#Botón eliminar
boton_eliminar = tk.Button(
    ventana,
    text="Eliminar tarea",
    command=eliminar_tarea
)

boton_eliminar.pack()

cargar_tareas()

ventana.mainloop()

conexion.close()