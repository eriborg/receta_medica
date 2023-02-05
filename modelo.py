from tkinter import messagebox
from datetime import datetime, date
import sqlite3 as sql
import re


# ##############################################
# MODELO
# ##############################################

# CONEXIÓN A LA BBDD
def conexion_db():
    con = sql.connect("receta_medica.db")
    return con


# CREA LA TABLA EN EL CASO QUE NO EXISTA
def crear_tabla():
    conexion = conexion_db()
    cursor = conexion.cursor()

    cursor.execute(
        """ SELECT count(name) FROM sqlite_master WHERE type='table' AND name='receta_medica' """
    )

    if cursor.fetchone()[0] != 1:

        cursor.execute(
            """
        CREATE TABLE receta_medica (
            receta_medica INTEGER PRIMARY KEY AUTOINCREMENT,
            medico TEXT NOT NULL, 
            cal_fec_pre TEXT NOT NULL,
            paciente TEXT NOT NULL,
            cal_fec_nac TEXT NOT NULL, 
            edad INTEGER, 
            cobertura TEXT NOT NULL, 
            diagnostico TEXT NOT NULL, 
            medicamento_1 TEXT NOT NULL, 
            medicamento_2 TEXT
        )
        """
        )

    conexion.commit()
    conexion.close()


# ALTA: de una receta médica
def generar_prescripcion(
    receta: tuple,
    tv,
):
    # 0= medico, 1=cal_fec_pre, 2=paciente, 3=cal_fec_nac, 4=edad,
    # 5=cobertura, 6=diagnostico, 7=medicamento_1, 8=medicamento_2
    datos = (
        receta[0].get().title().strip(),
        receta[1].get_date(),
        receta[2].get().title().strip(),
        receta[3].get_date(),
        receta[4].get(),
        receta[5].get().upper().strip(),
        receta[6].get().title().strip(),
        receta[7].get().strip(),
        receta[8].get().strip(),
    )

    error = validar_prescripcion(datos)

    if error != "":
        messagebox.showerror(title="Error", message=error)
    else:

        respuesta = messagebox.askokcancel(
            title="Generación de Receta Médica",
            message="¿Confirma los datos para Generar la Receta?",
        )
        if respuesta == True:

            con = conexion_db()
            cursor = con.cursor()
            print(datos)
            sql_insert = """INSERT INTO RECETA_MEDICA 
                (medico, cal_fec_pre, paciente, cal_fec_nac, edad, cobertura, diagnostico, medicamento_1, medicamento_2) 
                VALUES(?,?,?, ?,?,?,?, ?,? )"""
            cursor.execute(sql_insert, datos)
            con.commit()

            actualizar_treeview(tv)

            messagebox.showinfo(
                title="Alta", message="La receta fue generada exitosamente"
            )

            return True


# ACTUALIZACION: actualización de una receta médica
def actualizar_prescripcion(receta: tuple, tv):

    # 0= medico, 1=cal_fec_pre, 2=paciente, 3=cal_fec_nac, 4=edad,
    # 5=cobertura, 6=diagnostico, 7=medicamento_1, 8=medicamento_2,, 9=rec_med_id
    datos = (
        receta[0].get().title(),
        receta[1].get_date(),
        receta[2].get().title(),
        receta[3].get_date(),
        receta[4].get(),
        receta[5].get().upper(),
        receta[6].get().title(),
        receta[7].get(),
        receta[8].get(),
        receta[9].get(),
    )

    error = validar_prescripcion(datos)

    if error != "":
        messagebox.showerror(title="Error", message=error)
    else:

        respuesta = messagebox.askokcancel(
            title="Actualización de datos", message="¿Confirma los cambios a realizar?"
        )

        if respuesta == True:

            con = conexion_db()
            cursor = con.cursor()

            sql_uptade = """UPDATE RECETA_MEDICA 
                SET 
                    medico = ?,
                    cal_fec_pre = ?, 
                    paciente = ?, 
                    cal_fec_nac = ?,
                    edad = ?, 
                    cobertura = ?, 
                    diagnostico = ?, 
                    medicamento_1 = ?, 
                    medicamento_2 = ?         
                WHERE receta_medica = ?"""

            cursor.execute(sql_uptade, datos)
            con.commit()

            limpiar_campos(receta)

            actualizar_treeview(tv)

            messagebox.showinfo(
                title="Actualización", message="La receta fue actualizada exitosamente"
            )
            return True


# ELIMINACION:elimina la receta que el usuario ha seleccionado en el treeview
def eliminar_prescripcion(tv):

    valor = tv.selection()
    if len(valor) == 1:
        respuesta = messagebox.askyesno(
            title="Baja de Receta Médica",
            message="¿Confirma que desea eliminar la receta generada?",
        )
        if respuesta == True:
            item = tv.item(valor)
            print(item)
            print(item["text"])
            print(item["values"][0])
            mi_id = item["text"]

            con = conexion_db()
            cursor = con.cursor()
            data = (mi_id,)
            sql = "DELETE FROM RECETA_MEDICA WHERE RECETA_MEDICA = ?;"
            cursor.execute(sql, data)
            con.commit()
            tv.delete(valor)
            messagebox.showinfo(
                "Baja de Receta Médica",
                message="¡Receta Médica eliminada exitosamente!",
            )
        else:
            actualizar_treeview(tv)
    else:
        messagebox.showwarning(
            title="Atención", message="¡Debe seleccionar una receta a eliminar!"
        )


# ACTUALIZACION DE LA TREEVIEW
def actualizar_treeview(tv, str_busqueda=""):

    registros = tv.get_children()
    for reg in registros:
        tv.delete(reg)

    con = conexion_db()
    cursor = con.cursor()

    if len(str_busqueda) > 0:
        sql_cons = "SELECT * FROM RECETA_MEDICA WHERE lower(REPLACE(REPLACE(REPLACE(replace(paciente,'á','a'),'é','e'),'ó','o'),'ú','u')) LIKE lower(REPLACE(REPLACE(REPLACE(replace(?,'á','a'),'é','e'),'ó','o'),'ú','u'));"
        recetas = cursor.execute(sql_cons, ("%" + str_busqueda + "%",))
    else:
        sql_cons = "SELECT * FROM RECETA_MEDICA ORDER BY RECETA_MEDICA DESC"
        recetas = cursor.execute(sql_cons)

    resultados = recetas.fetchall()

    for fila in resultados:

        if fila[4] or fila[2]:
            fn = datetime.strptime(fila[4], "%Y-%m-%d")
            fp = datetime.strptime(fila[2], "%Y-%m-%d")
            fn_str = fn.date().strftime("%d/%m/%Y")
            fp_str = fp.date().strftime("%d/%m/%Y")

        tv.insert(
            "",
            0,
            text=fila[0],
            values=(
                fila[3],
                fn_str,
                fila[5],
                fila[6],
                fila[7],
                fp_str,
                fila[8],
                fila[9],
                fila[1],
            ),
        )


# LIMPIAR FORMULARIO
def limpiar_campos(receta: tuple):
    hoy = date.today()

    # 0=medico, 1=cal_fec_pre, 2=paciente, 3=cal_fec_nac, 4=edad,5=cobertura
    # 6=diagnostico, 7=medicamento_1, 8=medicamento_2,9= rec_med_id

    receta[0].set("")
    receta[1].set_date(hoy)
    receta[2].set("")
    receta[3].set_date(hoy),
    receta[4].set(0),
    receta[5].set(""),
    receta[6].set("")
    receta[7].set("")
    receta[8].set("")
    receta[9].set("")


# VALIDACION REGEX: valido que los campos de paciente y médico se completen solo con texto
def validar_prescripcion(datos: tuple):
    error = ""

    if not re.match("^[A-Za-záéíóú\s]+$", datos[2]):
        error = error + "error en el campo paciente\n"

    if not re.match("^[A-Za-záéíóú\s]+$", datos[0]):
        error = error + "error en el campo médico\n"

    return error


# CALCULAR LA EDAD DEL PACIENTE: edad del paciente en la fecha en la que se realiza la receta
def calcular_edad(f_nac, f_pre):

    mes_pre = int(f_pre.strftime("%m"))
    dia_pre = int(f_pre.strftime("%d"))
    mes_nac = int(f_nac.strftime("%m"))
    dia_nac = int(f_nac.strftime("%d"))
    anio_nac = int(f_nac.strftime("%Y"))
    anio_pre = int(f_pre.strftime("%Y"))
    if anio_nac >= anio_pre:
        return 0
    elif mes_nac < mes_pre:
        return anio_pre - anio_nac
    elif dia_nac <= dia_pre:
        return anio_pre - anio_nac
    else:
        return anio_pre - anio_nac - 1


## MAIN ##
try:
    crear_tabla()
except:
    print("Hay un error en la conexión")
