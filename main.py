from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# from tkinter.messagebox import *
from tkcalendar import Calendar, DateEntry
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
    datos: tuple,
    tv,
):

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

            limpiar_campos()

            actualizar_treeview(tv)

            messagebox.showinfo(
                title="Alta", message="La receta fue generada exitosamente"
            )


# ACTUALIZACION: actualización de una receta médica
def actualizar_prescripcion(datos: tuple, tv):

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

            limpiar_campos()

            actualizar_treeview(tv)

            messagebox.showinfo(
                title="Actualización", message="La receta fue actualizada exitosamente"
            )
            btn_gen_prescripcion.config(state="normal")
            btn_act_prescripcion.config(state="disabled")


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
def limpiar_campos():
    hoy = date.today()

    lbl_rec_med_id.config(text="")
    rec_med_id.set("")
    medico.set(""),
    paciente.set(""),
    cal_fec_nac.set_date(hoy),
    edad.set(0),
    cobertura.set(""),
    diagnostico.set("")
    cal_fec_pre.set_date(hoy),
    medicamento_1.set(""),
    medicamento_2.set("")


# BOTON CANCELAR
def cancelar(tv):
    respuesta = messagebox.askokcancel(
        title="Confirmación", message="¿Está seguro que desea cancelar?"
    )

    if respuesta == True:
        btn_gen_prescripcion.config(state="normal")
        btn_act_prescripcion.config(state="disabled")
        limpiar_campos()
        actualizar_treeview(tv)


# BOTON MODIFICAR: muestra los datos en pantalla para su modificación a partir de la selección de una receta
def modificar_prescripcion(tv):
    valor = tv.selection()
    if len(valor) == 1:
        item = tv.item(valor)
        mi_id = item["text"]

        btn_gen_prescripcion.config(state="disabled")
        btn_act_prescripcion.config(state="normal")

        lbl_rec_med_id.config(text="Receta Nº" + str(mi_id))
        rec_med_id.set(str(mi_id))
        medico.set(item["values"][8])
        paciente.set(item["values"][0])
        cal_fec_nac.set_date(item["values"][1])
        edad.set(item["values"][2])
        cobertura.set(item["values"][3])
        diagnostico.set(item["values"][4])
        cal_fec_pre.set_date(item["values"][5])
        medicamento_1.set(item["values"][6])
        medicamento_2.set(item["values"][7])
    else:
        messagebox.showwarning(
            title="Atención", message="Debe seleccionar una receta para modificar"
        )


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


# EVENTOS
# Descripción que se le muestra al usuario para que pueda buscar una receta por el nombre del paciente
def click_con(event):
    entr_consulta.delete(0, END)
    entr_consulta.config(foreground="black")


def on_focusout_con(event):
    if consulta.get() == "":
        entr_consulta.insert(0, "Ingrese Nombre del Paciente...")
        entr_consulta.config(foreground="grey")


# ejecuta el cálculo de la Edad del paciente
def on_focusout_fnac(event):
    edad.set(calcular_edad(cal_fec_nac.get_date(), cal_fec_pre.get_date()))


## MAIN ##

try:
    crear_tabla()
except:
    print("Hay un error en la conexión")

# ##############################################
# VISTA
# ##############################################

main = Tk()
main.geometry("1280x760")
main.title("Trabajo Final: Prescripción Médica")
main.config(bg="#f6f6f7")

# icon_rec_med.png
icono = PhotoImage(file="icon_rec_med.png")
main.iconphoto(True, icono)

# Estilos
color_boton = "#2d5b82"
col_bot_sec = "#D6DBDF"
color_etiqueta = "#2d5b82"
color_bg_eti = "#f6f6f7"
color_separador = "#2d5b82"
color_calendario = "#2d5b82"
color_fuente = "#f6f6f7"
fuente = ("calibri", 11, "normal")
fuente_lbl = ("calibri", 11, "bold")
w_ancho = 80

# Se definen las variables para tomar valores de los campos de entrada
(
    rec_med_id,
    medico,
    paciente,
    edad,
    cobertura,
    diagnostico,
    medicamento_1,
    medicamento_2,
) = (
    StringVar(),
    StringVar(),
    StringVar(),
    IntVar(),
    StringVar(),
    StringVar(),
    StringVar(),
    StringVar(),
)
today = date.today()

# ##############################################
# FORMULARIO
# ##############################################
lbl_rec_med_id = Label(
    main,
    text="",
    bg=color_etiqueta,
    fg=color_fuente,
    font=fuente,
    height=1,
    width=20,
)
lbl_rec_med_id.grid(row=0, column=0, columnspan=1, padx=1, pady=1, sticky=W + E)

titulo = Label(
    main,
    text="Ingrese los datos de la prescripción",
    bg=color_etiqueta,
    fg=color_fuente,
    font=fuente,
    height=1,
    width=80,
)
titulo.grid(row=0, column=1, columnspan=3, pady=1, sticky=W + E)

lbl_medico = Label(
    main, text="Nombre del Médico", font=fuente_lbl, width=20, bg=color_bg_eti
)
lbl_medico.grid(row=1, column=0, padx=1, pady=5, sticky=W)

entr_medico = Entry(
    main, textvariable=medico, width=40, font=fuente, highlightthickness=1
)
entr_medico.grid(row=1, column=1, padx=1, pady=5, sticky=W)


lbl_fec_pre = Label(
    main, text="Fecha de Prescripción", font=fuente_lbl, width=20, bg=color_bg_eti
)
lbl_fec_pre.grid(row=1, column=2, padx=1, pady=5, sticky=E)

cal_fec_pre = DateEntry(
    main,
    width=20,
    background=color_calendario,
    foreground="white",
    bd=2,
    date_pattern="dd/MM/yyyy",
    selectmode="day",
    firstweekday="sunday",
    mindate=today,
    maxdate=today,
    state="readonly",
)
cal_fec_pre.grid(row=1, column=3, padx=1, pady=5, sticky=W)
cal_fec_pre.set_date(today)


lbl_paciente = Label(
    main, text="Nombre del Paciente", font=fuente_lbl, width=20, bg=color_bg_eti
)
lbl_paciente.grid(row=2, column=0, padx=1, pady=5, sticky=W)

entr_paciente = Entry(
    main, textvariable=paciente, width=w_ancho, font=fuente, highlightthickness=1
)
entr_paciente.grid(row=2, column=1, padx=1, pady=5, sticky=W)

lbl_cobertura = Label(
    main, text="Cobertura Médica", font=fuente_lbl, width=20, bg=color_bg_eti
)
lbl_cobertura.grid(row=2, column=2, padx=1, pady=5, sticky=E)

cbox_cobert = ttk.Combobox(
    main,
    state="readonly",
    values=["PARTICULAR", "GALENO", "OSDE", "PAMI", "SWISS MEDICAL"],
    textvariable=cobertura,
)
cbox_cobert.grid(row=2, column=3, padx=1, pady=5, sticky=W)

lbl_fec_nac = Label(
    main, text="Fecha de Nacimiento", font=fuente_lbl, width=20, bg=color_bg_eti
)
lbl_fec_nac.grid(row=3, column=0, padx=1, pady=5, sticky=W)
sel = StringVar()

cal_fec_nac = DateEntry(
    main,
    width=20,
    background=color_calendario,
    foreground="white",
    bd=2,
    date_pattern="dd/MM/yyyy",
    firstweekday="sunday",
    selectmode="day",
    maxdate=today,
    state="readonly",
)
cal_fec_nac.grid(row=3, column=1, padx=1, pady=5, sticky=W)
cal_fec_nac.bind("<FocusOut>", on_focusout_fnac)

lbl_edad = Label(main, text="Edad", font=fuente_lbl, width=20, bg=color_bg_eti)
lbl_edad.grid(row=3, column=2, padx=1, pady=5, sticky=E)

entr_edad = Entry(
    main, textvariable=edad, width=20, state=DISABLED, highlightthickness=1
)
entr_edad.grid(row=3, column=3, padx=1, pady=5, sticky=W)

lbl_diagnostico = Label(
    main, text="Diagnóstico", font=fuente_lbl, width=20, bg=color_bg_eti
)
lbl_diagnostico.grid(row=4, column=0, padx=1, pady=5, sticky=W)

entr_diagnostico = Entry(
    main, textvariable=diagnostico, width=w_ancho, font=fuente, highlightthickness=1
)
entr_diagnostico.grid(row=4, column=1, padx=1, pady=5, sticky=W)

lbl_medicamento_1 = Label(
    main, text="Medicamento 1", font=fuente_lbl, width=20, bg=color_bg_eti
)
lbl_medicamento_1.grid(row=5, column=0, padx=1, pady=5, sticky=W)

entr_medic_1 = Entry(
    main, textvariable=medicamento_1, width=w_ancho, font=fuente, highlightthickness=1
)
entr_medic_1.grid(row=5, column=1, padx=1, pady=5, sticky=W)

lbl_medicamento_2 = Label(
    main, text="Medicamento 2", font=fuente_lbl, width=20, bg=color_bg_eti
)
lbl_medicamento_2.grid(row=6, column=0, padx=1, pady=5, sticky=W)

entr_medic_2 = Entry(
    main, textvariable=medicamento_2, width=w_ancho, font=fuente, highlightthickness=1
)
entr_medic_2.grid(row=6, column=1, padx=1, pady=5, sticky=W)

# BOTONES
btn_gen_prescripcion = Button(
    main,
    text="Generar Prescripción",
    command=lambda: generar_prescripcion(
        (
            medico.get().title().strip(),
            cal_fec_pre.get_date(),
            paciente.get().title().strip(),
            cal_fec_nac.get_date(),
            edad.get(),
            cobertura.get().upper().strip(),
            diagnostico.get().title().strip(),
            medicamento_1.get().strip(),
            medicamento_2.get().strip(),
        ),
        tv_prescr,
    ),
    padx=2,
    pady=1,
    activebackground="#f6f6f7",
    activeforeground=color_boton,
    background=color_boton,
    foreground="#f6f6f7",
    anchor=CENTER,
    font=fuente,
    height=1,
    width=20,
)
btn_gen_prescripcion.grid(row=7, column=0, padx=1)

btn_act_prescripcion = Button(
    main,
    text="Actualizar Prescripción",
    command=lambda: actualizar_prescripcion(
        (
            medico.get().title(),
            cal_fec_pre.get_date(),
            paciente.get().title(),
            cal_fec_nac.get_date(),
            edad.get(),
            cobertura.get().upper(),
            diagnostico.get().title(),
            medicamento_1.get(),
            medicamento_2.get(),
            rec_med_id.get(),
        ),
        tv_prescr,
    ),
    padx=2,
    pady=1,
    activebackground="#f6f6f7",
    activeforeground=color_boton,
    background=color_boton,
    foreground="#f6f6f7",
    anchor=CENTER,
    font=fuente,
    height=1,
    width=20,
    state="disabled",
)
btn_act_prescripcion.grid(row=7, column=1, padx=1, sticky=W)

btn_cancelar = Button(
    main,
    text="Cancelar",
    command=lambda: cancelar(
        tv_prescr,
    ),
    padx=2,
    pady=1,
    activebackground=color_boton,
    activeforeground=col_bot_sec,
    background=col_bot_sec,
    foreground=color_boton,
    anchor=CENTER,
    font=fuente,
    height=1,
    width=20,
)
btn_cancelar.grid(row=7, column=2, padx=1, sticky=W)

ttk.Separator(main, orient=HORIZONTAL).grid(
    row=8, column=0, columnspan=4, sticky=W + E, padx=2, pady=10
)

# BOTON MODIFICAR RECETA: a partir de la selección de un paciente
boton_modificar = Button(
    main,
    text="Modificar",
    command=lambda: modificar_prescripcion(tv_prescr),
    padx=2,
    pady=1,
    activebackground="#f6f6f7",
    activeforeground=color_boton,
    background=color_boton,
    foreground="#f6f6f7",
    anchor=CENTER,
    font=fuente,
    height=1,
    width=20,
)
boton_modificar.grid(row=9, column=0, pady=10)

# ENTRADA DE CONSULTA: Buscar recetas por nombre de paciente
consulta = StringVar()
consulta.set("Ingrese Nombre del Paciente")
entr_consulta = Entry(
    main, textvariable=consulta, width=w_ancho, font=fuente, foreground="grey"
)
entr_consulta.grid(row=9, column=1, pady=10, sticky=W)
entr_consulta.bind("<Button-1>", click_con)
entr_consulta.bind("<FocusOut>", on_focusout_con)


# BOTON DE CONSULTA: Ejecuta la consulta de las recetas de 1 paciente
boton_consulta = Button(
    main,
    text="Consultar",
    command=lambda: actualizar_treeview(tv_prescr, consulta.get().strip()),
    padx=1,
    pady=1,
    activebackground="#f6f6f7",
    activeforeground=color_boton,
    background=color_boton,
    foreground="#f6f6f7",
    anchor=CENTER,
    font=fuente,
    height=1,
    width=20,
)
boton_consulta.grid(row=9, column=2, pady=10, sticky=W)


# BOTON DE BAJA: botón para eliminar una receta médica
boton_baja = Button(
    main,
    text="Baja",
    command=lambda: eliminar_prescripcion(tv_prescr),
    padx=1,
    pady=1,
    activebackground="#f6f6f7",
    activeforeground=color_boton,
    background=color_boton,
    foreground="#f6f6f7",
    anchor=CENTER,
    font=fuente,
    height=1,
    width=20,
)
boton_baja.grid(row=9, column=3, padx=15, pady=10, sticky=E)

# ##############################################
# TREEVIEW
# ##############################################

style = ttk.Style(main)
style.theme_use("clam")
style.configure("Treeview.Heading", background=color_etiqueta, foreground="white")

tv_prescr = ttk.Treeview(
    main,
    columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9"),
    height=18,
)

tv_prescr.column("#0", width=30, anchor=W)
tv_prescr.column("col1", width=200, anchor=W)
tv_prescr.column("col2", width=75, anchor=E)
tv_prescr.column("col3", width=40, anchor=E)
tv_prescr.column("col4", width=160, anchor=W)
tv_prescr.column("col5", width=200, anchor=W)
tv_prescr.column("col6", width=75, anchor=E)
tv_prescr.column("col7", width=200, anchor=W)
tv_prescr.column("col8", width=200, anchor=W)
tv_prescr.column("col9", width=80, anchor=W)

tv_prescr.heading("#0", text="Id", anchor=CENTER)
tv_prescr.heading("col1", text="Nombre Paciente", anchor=CENTER)
tv_prescr.heading("col2", text="Fecha Nac.", anchor=CENTER)
tv_prescr.heading("col3", text="Edad", anchor=CENTER)
tv_prescr.heading("col4", text="Cobertura Médica", anchor=CENTER)
tv_prescr.heading("col5", text="Diagnóstico", anchor=CENTER)
tv_prescr.heading("col6", text="Fecha Prescr.", anchor=CENTER)
tv_prescr.heading("col7", text="Medicamento 1", anchor=CENTER)
tv_prescr.heading("col8", text="Medicamento 2", anchor=CENTER)
tv_prescr.heading("col9", text="Médico", anchor=CENTER)


actualizar_treeview(tv_prescr)

tv_prescr.grid(row=20, column=0, columnspan=4, padx=10, pady=5, sticky=E)

main.mainloop()
