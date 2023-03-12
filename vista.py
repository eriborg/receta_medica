from tkinter import (    
    CENTER,
    DISABLED,
    END,
    HORIZONTAL,
    Button,
    PhotoImage,
    messagebox,
    ttk,
)
from tkinter import StringVar
from tkinter import IntVar
from tkinter import Label
from tkinter import Entry
from datetime import datetime, date
from tkcalendar import Calendar, DateEntry
from crud_receta_medica import CrudRecetaMedica

# ##############################################
# VISTA
# ##############################################

class MainWindow(ttk.Frame):    

    def __init__(self, main_window):
        """
            vista.py:
            Vista de la pantalla principal de Receta Médica.
        """
        super().__init__(main_window)
        self.rec_med = CrudRecetaMedica()
        self.main = main_window

        self.main.geometry("1280x760")
        self.main.title("Trabajo Final: Receta Médica")
        self.main.config(bg="#f6f6f7")

        # icon_rec_med.png
        self.icono = PhotoImage(file="icon_rec_med.png")
        self.main.iconphoto(True, self.icono)

        # Estilos
        self.color_boton = "#2d5b82"
        self.col_bot_sec = "#D6DBDF"
        self.color_etiqueta = "#2d5b82"
        self.color_bg_eti = "#f6f6f7"
        self.color_separador = "#2d5b82"
        self.color_calendario = "#2d5b82"
        self.color_fuente = "#f6f6f7"
        self.fuente = ("calibri", 11, "normal")
        self.fuente_lbl = ("calibri", 11, "bold")
        self.w_ancho = 80

        #variables tkinter
        self.rec_med_id =  StringVar()
        self.medico = StringVar()
        self.paciente = StringVar()
        self.edad =IntVar()
        self.cobertura = StringVar()
        self.diagnostico = StringVar()
        self.medicamento_1 = StringVar()
        self.medicamento_2 = StringVar()
        self.today = date.today()

        # ##############################################
        # FORMULARIO
        # ##############################################
        self.rec_med_id.set("")
        self.lbl_rec_med_id = Label(
            self.main,
            text="",
            background=self.color_etiqueta,
            foreground=self.color_fuente,
            font=self.fuente,
            width=20,
        )
        self.lbl_rec_med_id.grid(row=0, column=0, columnspan=1, padx=1, pady=1, sticky="w" + "e")

        self.titulo = Label(
            self.main,
            text="Ingrese los datos de la prescripción",
            background=self.color_etiqueta,
            foreground=self.color_fuente,
            font=self.fuente,
            width=80,
        )
        self.titulo.grid(row=0, column=1, columnspan=3, pady=1, sticky="w" + "e")

        self.lbl_medico = Label(
            self.main, text="Nombre del Médico", font=self.fuente_lbl, width=20, background=self.color_bg_eti
        )
        self.lbl_medico.grid(row=1, column=0, padx=1, pady=5, sticky="w")

        self.entr_medico = Entry(
            self.main, textvariable=self.medico, width=40, font=self.fuente, highlightthickness=1
        )
        self.entr_medico.grid(row=1, column=1, padx=1, pady=5, sticky="w")

        self.lbl_fec_pre = Label(
            self.main, text="Fecha de Prescripción", font=self.fuente_lbl, width=20, bg=self.color_bg_eti
        )
        self.lbl_fec_pre.grid(row=1, column=2, padx=1, pady=5, sticky="e")

        self.cal_fec_pre = DateEntry(
            self.main,
            width=20,
            background=self.color_calendario,
            foreground="white",
            bd=2,
            date_pattern="dd/MM/yyyy",
            selectmode="day",
            firstweekday="sunday",
            mindate=self.today,
            maxdate=self.today,
            state="readonly",
        )
        self.cal_fec_pre.grid(row=1, column=3, padx=1, pady=5, sticky="w")
        self.cal_fec_pre.set_date(self.today)

        self.lbl_paciente = Label(
            self.main, text="Nombre del Paciente", font=self.fuente_lbl, width=20, bg=self.color_bg_eti
        )
        self.lbl_paciente.grid(row=2, column=0, padx=1, pady=5, sticky="w")

        self.entr_paciente = Entry(
            self.main, textvariable=self.paciente, width=self.w_ancho, font=self.fuente, highlightthickness=1
        )
        self.entr_paciente.grid(row=2, column=1, padx=1, pady=5, sticky="w")

        self.lbl_cobertura = Label(
            self.main, text="Cobertura Médica", font=self.fuente_lbl, width=20, bg=self.color_bg_eti
        )
        self.lbl_cobertura.grid(row=2, column=2, padx=1, pady=5, sticky="e")

        self.cbox_cobert = ttk.Combobox(
            self.main,
            state="readonly",
            values=["PARTICULAR", "GALENO", "OSDE", "PAMI", "SWISS MEDICAL"],
            textvariable=self.cobertura,
        )
        self.cbox_cobert.grid(row=2, column=3, padx=1, pady=5, sticky="w")

        self.lbl_fec_nac = Label(
            self.main, text="Fecha de Nacimiento", font=self.fuente_lbl, width=20, bg=self.color_bg_eti
        )
        self.lbl_fec_nac.grid(row=3, column=0, padx=1, pady=5, sticky="w")
        self.sel = StringVar()

        self.cal_fec_nac = DateEntry(
            self.main,
            width=20,
            background=self.color_calendario,
            foreground="white",
            bd=2,
            date_pattern="dd/MM/yyyy",
            firstweekday="sunday",
            selectmode="day",
            maxdate=self.today,
            state="readonly",
        )
        self.cal_fec_nac.grid(row=3, column=1, padx=1, pady=5, sticky="w")
        self.cal_fec_nac.bind("<FocusOut>", self.on_focusout_fnac)

        self.lbl_edad = Label(self.main, text="Edad", font=self.fuente_lbl, width=20, bg=self.color_bg_eti)
        self.lbl_edad.grid(row=3, column=2, padx=1, pady=5, sticky="e")

        self.entr_edad = Entry(
            self.main, textvariable=self.edad, width=20, state=DISABLED, highlightthickness=1
        )
        self.entr_edad.grid(row=3, column=3, padx=1, pady=5, sticky="w")

        self.lbl_diagnostico = Label(
            self.main, text="Diagnóstico", font=self.fuente_lbl, width=20, bg=self.color_bg_eti
        )
        self.lbl_diagnostico.grid(row=4, column=0, padx=1, pady=5, sticky="w")

        self.entr_diagnostico = Entry(
            self.main, textvariable=self.diagnostico, width=self.w_ancho, font=self.fuente, highlightthickness=1
        )
        self.entr_diagnostico.grid(row=4, column=1, padx=1, pady=5, sticky="w")

        self.lbl_medicamento_1 = Label(
            self.main, text="Medicamento 1", font=self.fuente_lbl, width=20, bg=self.color_bg_eti
        )
        self.lbl_medicamento_1.grid(row=5, column=0, padx=1, pady=5, sticky="w")

        self.entr_medic_1 = Entry(
            self.main,
            textvariable=self.medicamento_1,
            width=self.w_ancho,
            font=self.fuente,
            highlightthickness=1,
        )
        self.entr_medic_1.grid(row=5, column=1, padx=1, pady=5, sticky="w")

        self.lbl_medicamento_2 = Label(
            self.main, text="Medicamento 2", font=self.fuente_lbl, width=20, bg=self.color_bg_eti
        )
        self.lbl_medicamento_2.grid(row=6, column=0, padx=1, pady=5, sticky="w")

        self.entr_medic_2 = Entry(
            self.main,
            textvariable=self.medicamento_2,
            width=self.w_ancho,
            font=self.fuente,
            highlightthickness=1,
        )
        self.entr_medic_2.grid(row=6, column=1, padx=1, pady=5, sticky="w")

        """
        # Botón Generar Prescripción, llama a la vista_alta()
        """
        self.btn_gen_prescripcion = Button(
            self.main,
            text="Generar Prescripción",
            command=lambda: self.vista_alta(),
            padx=2,
            pady=1,
            activebackground="#f6f6f7",
            activeforeground=self.color_boton,
            background=self.color_boton,
            foreground="#f6f6f7",
            anchor=CENTER,
            font=self.fuente,
            height=1,
            width=20,
        )
        self.btn_gen_prescripcion.grid(row=7, column=0, padx=1)

        self.btn_act_prescripcion = Button(
            self.main,
            text="Actualizar Prescripción",
            command=lambda: self.vista_actualizacion(),
            padx=2,
            pady=1,
            activebackground="#f6f6f7",
            activeforeground=self.color_boton,
            background=self.color_boton,
            foreground="#f6f6f7",
            anchor=CENTER,
            font=self.fuente,
            height=1,
            width=20,
            state="disabled",
        )
        self.btn_act_prescripcion.grid(row=7, column=1, padx=1, sticky="w")

        self.btn_cancelar = Button(
            self.main,
            text="Cancelar",
            command=lambda: self.vista_cancelar(),
            padx=2,
            pady=1,
            activebackground=self.color_boton,
            activeforeground=self.col_bot_sec,
            background=self.col_bot_sec,
            foreground=self.color_boton,
            anchor=CENTER,
            font=self.fuente,
            height=1,
            width=20,
        )
        self.btn_cancelar.grid(row=7, column=2, padx=1, sticky="w")

        ttk.Separator(self.main, orient=HORIZONTAL).grid(
            row=8, column=0, columnspan=4, sticky="w" + "e", padx=2, pady=10
        )

        # BOTON MODIFICAR RECETA: a partir de la selección de un paciente
        self.boton_modificar = Button(
            self.main,
            text="Modificar",
            command=lambda: self.vista_modicacion(),
            padx=2,
            pady=1,
            activebackground="#f6f6f7",
            activeforeground=self.color_boton,
            background=self.color_boton,
            foreground="#f6f6f7",
            anchor=CENTER,
            font=self.fuente,
            height=1,
            width=20,
        )
        self.boton_modificar.grid(row=9, column=0, pady=10)

        # ENTRADA DE CONSULTA: Buscar recetas por nombre de paciente
        self.consulta = StringVar()
        self.consulta.set("Ingrese Nombre del Paciente")
        self.entr_consulta = Entry(
            self.main, textvariable=self.consulta, width=self.w_ancho, font=self.fuente, foreground="grey"
        )
        self.entr_consulta.grid(row=9, column=1, pady=10, sticky="w")
        self.entr_consulta.bind("<Button-1>", self.click_con)
        self.entr_consulta.bind("<FocusOut>", self.on_focusout_con)

        # BOTON DE CONSULTA: Ejecuta la consulta de las recetas de 1 paciente
        self.boton_consulta = Button(
            self.main,
            text="Consultar",
            command=lambda: self.vista_consulta(),
            padx=1,
            pady=1,
            activebackground="#f6f6f7",
            activeforeground=self.color_boton,
            background=self.color_boton,
            foreground="#f6f6f7",
            anchor=CENTER,
            font=self.fuente,
            height=1,
            width=20,
        )
        self.boton_consulta.grid(row=9, column=2, pady=10, sticky="w")

    # BOTON DE BAJA: botón para eliminar una receta médica
        self.boton_baja = Button(
            self.main,
            text="Baja",
            command=lambda: self.vista_baja(),
            padx=1,
            pady=1,
            activebackground="#f6f6f7",
            activeforeground=self.color_boton,
            background=self.color_boton,
            foreground="#f6f6f7",
            anchor=CENTER,
            font=self.fuente,
            height=1,
            width=20,
        )
        self.boton_baja.grid(row=9, column=3, padx=15, pady=10, sticky="e")

        # ##############################################
        # TREEVIEW
        # ##############################################

        self.style = ttk.Style(self.main)
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", background=self.color_etiqueta, foreground="white")

        self.tv_prescr = ttk.Treeview(
            self.main,
            columns=(
                "col1",
                "col2",
                "col3",
                "col4",
                "col5",
                "col6",
                "col7",
                "col8",
                "col9",
            ),
            height=18,
        )

        self.tv_prescr.column("#0", width=30, anchor="w")
        self.tv_prescr.column("col1", width=200, anchor="w")
        self.tv_prescr.column("col2", width=75, anchor="e")
        self.tv_prescr.column("col3", width=40, anchor="e")
        self.tv_prescr.column("col4", width=160, anchor="w")
        self.tv_prescr.column("col5", width=200, anchor="w")
        self.tv_prescr.column("col6", width=75, anchor="e")
        self.tv_prescr.column("col7", width=200, anchor="w")
        self.tv_prescr.column("col8", width=200, anchor="w")
        self.tv_prescr.column("col9", width=80, anchor="w")

        self.tv_prescr.heading("#0", text="Id", anchor=CENTER)
        self.tv_prescr.heading("col1", text="Nombre Paciente", anchor=CENTER)
        self.tv_prescr.heading("col2", text="Fecha Nac.", anchor=CENTER)
        self.tv_prescr.heading("col3", text="Edad", anchor=CENTER)
        self.tv_prescr.heading("col4", text="Cobertura Médica", anchor=CENTER)
        self.tv_prescr.heading("col5", text="Diagnóstico", anchor=CENTER)
        self.tv_prescr.heading("col6", text="Fecha Prescr.", anchor=CENTER)
        self.tv_prescr.heading("col7", text="Medicamento 1", anchor=CENTER)
        self.tv_prescr.heading("col8", text="Medicamento 2", anchor=CENTER)
        self.tv_prescr.heading("col9", text="Médico", anchor=CENTER)

        self.vista_tv()

        self.tv_prescr.grid(row=20, column=0, columnspan=4, padx=10, pady=5, sticky="e")

    # EVENTOS    
    def click_con(self,event):
        """
            Evento que al hacer click en el campo consulta No  se muestra el texto "Ingrese Nombre del Paciente..."
            
            :param event: on click
	    """
        self.entr_consulta.delete(0, END)
        self.entr_consulta.config(foreground="black")

    def on_focusout_con(self,event):
        """
            Evento que al salir del foco del campo consulta se muestra el texto "Ingrese Nombre del Paciente..."            
            
            :param event: on focus out
	    """
        if self.consulta.get() == "":
            self.entr_consulta.insert(0, "Ingrese Nombre del Paciente...")
            self.entr_consulta.config(foreground="grey")

    # ejecuta el cálculo de la Edad del paciente
    def on_focusout_fnac(self,event):
        """
            Evento que al salir del foco del campo fecha Nacimiento se calcula la edad del paciente            
            
            :param event: on focus out
	    """
        self.cal_edad = self.rec_med.calcular_edad(self.cal_fec_nac.get_date(), self.cal_fec_pre.get_date())
        self.edad.set(self.cal_edad)
   
    def vista_tv(self,):
        """
            Vista de actualización del Treeview de TKinter
	    """
        self.rec_med.actualizar_treeview(self.tv_prescr)

    def vista_alta(self,):
        """
            Vista Alta de una receta electrónica
	    """

        alta_receta = self.rec_med.generar_prescripcion(
            (self.medico,
             self.cal_fec_pre,
             self.paciente,
             self.cal_fec_nac,
             self.edad,
             self.cobertura,
             self.diagnostico,
             self.medicamento_1,
             self.medicamento_2,
             self.rec_med_id,),
             self.tv_prescr)

        if alta_receta == True:
            self.rec_med.limpiar_campos((self.medico,
             self.cal_fec_pre,
             self.paciente,
             self.cal_fec_nac,
             self.edad,
             self.cobertura,
             self.diagnostico,
             self.medicamento_1,
             self.medicamento_2,
             self.rec_med_id,))
            self.lbl_rec_med_id.config(text="")

    def vista_modicacion(
        self,        
    ): 
        """
            Vista Modificación: muestra los datos en pantalla para su modificación a partir de la selección de una receta
	    """      
        valor = self.tv_prescr.selection()
        
        if len(valor) == 1:
            item = self.tv_prescr.item(valor)
            mi_id = item["text"]

            self.btn_gen_prescripcion.config(state="disabled")
            self.btn_act_prescripcion.config(state="normal")
            self.lbl_rec_med_id.config(text="Receta Nº" + str(mi_id))

            # 0=rec_med_id, 1=medico,2=paciente, 3=cal_fec_nac, 4=edad, 5=cobertura
            # 6=diagnostico, 7=cal_fec_pre, 8=medicamento_1, 9=medicamento_2            
            self.rec_med_id.set(str(mi_id))
            self.medico.set(item["values"][8])
            self.paciente.set(item["values"][0])
            self.cal_fec_nac.set_date(item["values"][1])
            self.edad.set(item["values"][2])
            self.cobertura.set(item["values"][3])
            self.diagnostico.set(item["values"][4])
            self.cal_fec_pre.set_date(item["values"][5])
            self.medicamento_1.set(item["values"][6])
            self.medicamento_2.set(item["values"][7])
        else:
            messagebox.showwarning(
                title="Atención", message="Debe seleccionar una receta para modificar"
            )

    def vista_cancelar(self,):
        """
            Vista CANCELAR: cancela la operación que se estaba intentando hacer ya sea de crear o actualizar una receta
	    """

        respuesta = messagebox.askokcancel(
            title="Confirmación", message="¿Está seguro que desea cancelar?"
        )

        if respuesta == True:
            self.btn_gen_prescripcion.config(state="normal")
            self.btn_act_prescripcion.config(state="disabled")
            self.rec_med.limpiar_campos((
                    self.medico,
                    self.cal_fec_pre,
                    self.paciente,
                    self.cal_fec_nac,
                    self.edad,
                    self.cobertura,
                    self.diagnostico,
                    self.medicamento_1,
                    self.medicamento_2,
                    self.rec_med_id,
                ))
            self.rec_med.actualizar_treeview(self.tv_prescr)


    def vista_actualizacion(self,):
        """
            Vista Actualización: ejecuta el método de actualizar_prescripcion para modificar los datos de una receta médica existente 
            a partir de los datos ingresados por el usuario
	    """

        actual_receta = self.rec_med.actualizar_prescripcion(
                   (self.medico,
                    self.cal_fec_pre,
                    self.paciente,
                    self.cal_fec_nac,
                    self.edad,
                    self.cobertura,
                    self.diagnostico,
                    self.medicamento_1,
                    self.medicamento_2,
                    self.rec_med_id,),
                    self.tv_prescr)

        if actual_receta == True:
            self.btn_gen_prescripcion.config(state="normal")
            self.btn_act_prescripcion.config(state="disabled")

    def vista_baja(self):
        """
            Vista Baja: ejecuta el método de eliminar_prescripcion para eliminar una receta a partir
            de la fila seleccionada por el usuario en la treeview
	    """
        self.rec_med.eliminar_prescripcion(self.tv_prescr)
    
    def vista_consulta(self,):
        """
            Vista Consulta: ejecuta el método de actualizar_treeview para filtrar por paciente las recetas que
            se le hayan prescripto 
	    """
        self.rec_med.actualizar_treeview(self.tv_prescr, self.consulta.get().strip())