import mysql.connector
from reportlab.pdfgen import canvas
from tkinter import messagebox

conexion = mysql.connector.connect(
    host="localhost",        
    user="root",            
    password="",             
    database="sala_computacion" #nombre de la base
)

cursor = conexion.cursor()


#esto trae TODAS las computadoras de la base (comandos vistos el primer ejercicio)

def obtener_computadoras():
    cursor.execute("SELECT * FROM computadoras")
    return cursor.fetchall()
        #fetchall() sirve para traerte todos los resultados de una consulta

#agrega las computadoras a partir de los estruturado en la base de datos

def agregar_computadora(nombre, ip, marca, fecha, estado):
    try:
        sql = """
        INSERT INTO computadoras(nombre, ip, marca, fecha_verificacion, estado)
        VALUES (%s,%s,%s,%s,%s)
        """
            # %s es un lugar vacío
        valores = (nombre, ip, marca, fecha, estado)

        cursor.execute(sql, valores)
        conexion.commit()  # guarda los cambios

    except Exception as error:
        messagebox.showerror("Error", str(error))

#borra una computadora por su id

def eliminar_computadora(id_pc):
    try:
        sql = "DELETE FROM computadoras WHERE id=%s"
        cursor.execute(sql, (id_pc,))
        conexion.commit()

    except Exception as error:
        messagebox.showerror("Error", str(error))


#actualiza los datos de una computadora

def actualizar_computadora(id_pc, nombre, ip, marca, fecha, estado):
    try:
        sql = """
        UPDATE computadoras
        SET nombre=%s,
            ip=%s,
            marca=%s,
            fecha_verificacion=%s,
            estado=%s
        WHERE id=%s
        """

        valores = (nombre, ip, marca, fecha, estado, id_pc)

        cursor.execute(sql, valores)
        conexion.commit()

    except Exception as error:
        messagebox.showerror("Error", str(error))


#crea un archivo PDF con todas las computadoras q pusimos. funciones y algunos comandos para que python nos devuelva un pdf hecho y derecho 

def generar_reporte_pdf():
    try:
        pdf = canvas.Canvas("reporte_computadoras.pdf")

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(180, 800, "REPORTE DE COMPUTADORAS")

        #altura donde empieza a escribir

        cursor.execute("SELECT * FROM computadoras")
        datos = cursor.fetchall()

        pdf.setFont("Helvetica", 10)

        for pc in datos:
            #convertimos la fila en texto
            texto = f"{pc[0]} | {pc[1]} | {pc[2]} | {pc[3]} | {pc[4]} | {pc[5]}"

            pdf.drawString(30, y, texto)
            y -= 20  # baja una línea

            #si llega abajo de la hoja, crea otra página
            if y < 40:
                pdf.showPage()
                y = 800

        pdf.save()

        messagebox.showinfo("OK", "PDF creado correctamente")

    except Exception as error:
        messagebox.showerror("Error", str(error))