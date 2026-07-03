import tkinter as tk
from tkinter import messagebox
import backend as db

def cargar():
    lista.delete(0, tk.END)
    for pc in db.obtener_computadoras():
        lista.insert(tk.END, pc)

def agregar():
    if nombre.get() == "" or ip.get() == "":
        messagebox.showwarning("Aviso", "Complete los campos")
        return

    db.agregar_computadora(
        nombre.get(),
        ip.get(),
        marca.get(),
        fecha.get(),
        estado.get()
    )

    limpiar()
    cargar()


def eliminar():
    if not lista.curselection():
        return

    pc = lista.get(lista.curselection()[0])
    db.eliminar_computadora(pc[0])

    cargar()

def actualizar():
    if not lista.curselection():
        return

    pc = lista.get(lista.curselection()[0])

    db.actualizar_computadora(
        pc[0],
        nombre.get(),
        ip.get(),
        marca.get(),
        fecha.get(),
        estado.get()
    )

    limpiar()
    cargar()

def seleccionar(event):
    if not lista.curselection():
        return

    pc = lista.get(lista.curselection()[0])

    nombre.delete(0, tk.END)
    nombre.insert(0, pc[1])

    ip.delete(0, tk.END)
    ip.insert(0, pc[2])

    marca.delete(0, tk.END)
    marca.insert(0, pc[3])

    fecha.delete(0, tk.END)
    fecha.insert(0, pc[4])

    estado.delete(0, tk.END)
    estado.insert(0, pc[5])

def limpiar():
    nombre.delete(0, tk.END)
    ip.delete(0, tk.END)
    marca.delete(0, tk.END)
    fecha.delete(0, tk.END)
    estado.delete(0, tk.END)


ventana = tk.Tk()
ventana.title("Sala de Computación")
ventana.geometry("650x400")


tk.Label(ventana, text="Nombre").grid(row=0, column=0)
nombre = tk.Entry(ventana)
nombre.grid(row=0, column=1)

tk.Label(ventana, text="IP").grid(row=1, column=0)
ip = tk.Entry(ventana)
ip.grid(row=1, column=1)

tk.Label(ventana, text="Marca").grid(row=2, column=0)
marca = tk.Entry(ventana)
marca.grid(row=2, column=1)

tk.Label(ventana, text="Fecha").grid(row=3, column=0)
fecha = tk.Entry(ventana)
fecha.grid(row=3, column=1)

tk.Label(ventana, text="Estado").grid(row=4, column=0)
estado = tk.Entry(ventana)
estado.grid(row=4, column=1)


tk.Button(ventana, text="Agregar", command=agregar).grid(row=5, column=0)
tk.Button(ventana, text="Actualizar", command=actualizar).grid(row=5, column=1)
tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=5, column=2)
tk.Button(ventana, text="PDF", command=db.generar_reporte_pdf).grid(row=5, column=3)


lista = tk.Listbox(ventana, width=80)
lista.grid(row=6, column=0, columnspan=4)

lista.bind("<<ListboxSelect>>", seleccionar)

cargar()

ventana.mainloop()