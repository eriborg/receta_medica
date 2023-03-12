from tkinter import messagebox
from datetime import datetime, date
import re
import sqlite3 
from peewee import *
from peewee import fn
from receta_medica import *

# ##############################################
# MODELO
# ##############################################

class CrudRecetaMedica:         

    def __init__(self):
        pass
      
    # generar_prescripcion: Alta de una receta médica
    def generar_prescripcion(self,
        receta: tuple,
        tv,
    ):
        """
            Genera o da de Alta una nueva receta médica.
        
            :param receta: (0= medico, 1=cal_fec_pre, 2=paciente, 3=cal_fec_nac, 4=edad,
                        5=cobertura, 6=diagnostico, 7=medicamento_1, 8=medicamento_2)
	    """
        msg_error = ""
        try:
            medico = receta[0].get().title().strip() 
            self.validar_prescripcion(medico, "medico")

        except Exception as e:
            msg_error += str(e)
            self.log_text(str(e), "[ALTA]")            

        try:
            paciente = receta[2].get().title().strip()
            self.validar_prescripcion(paciente, "paciente")

        except Exception as e:
            msg_error += str(e)
            self.log_text(str(e), "[ALTA]")            
        
        if msg_error != "" :
            messagebox.showerror(title="Error", message=msg_error)
            print(msg_error)        
        else:
            rec_med = RecetaMedica()

            respuesta = messagebox.askokcancel(
                title="Generación de Receta Médica",
                message="¿Confirma los datos para Generar la Receta?",
            )

            if respuesta == True:

                rec_med.medico = medico
                rec_med.f_prescripcion = receta[1].get_date()
                rec_med.nombre_paciente = paciente
                rec_med.f_nac_pac = receta[3].get_date()
                rec_med.edad = receta[4].get()
                rec_med.cobertura = receta[5].get().upper().strip()
                rec_med.diagnostico = receta[6].get().title().strip()
                rec_med.medicamento_1 = receta[7].get().strip()
                rec_med.medicamento_2 = receta[8].get().strip()

            rec_med.save()

            self.actualizar_treeview(tv)

            messagebox.showinfo(
                    title="Alta", message="La receta fue generada exitosamente"
            )

            return True    
 
    # ACTUALIZACION DE LA TREEVIEW
    def actualizar_treeview(self, tv, str_busqueda=""):
        """
            Actualiza la treeview de Tkinter con todas las recetas almacenadas.
        
            :param tv: (0= medico, 1=cal_fec_pre, 2=paciente, 3=cal_fec_nac, 4=edad,
                        5=cobertura, 6=diagnostico, 7=medicamento_1, 8=medicamento_2)
            :param str_busqueda: por defecto viene vacío
	    """
        
        registros = tv.get_children()
        for reg in registros:
            tv.delete(reg)

        if len(str_busqueda) > 0:       
            resultados = RecetaMedica.select().where(RecetaMedica.nombre_paciente.like("*"+str_busqueda+"*"))          
        else:
            resultados = RecetaMedica.select()

        for fila in resultados:
            
            tv.insert("",0,
                text=fila.rec_med_id,
                values=(
                    fila.nombre_paciente,
                    fila.f_nac_pac.strftime("%d/%m/%Y"),
                    fila.edad,
                    fila.cobertura,
                    fila.diagnostico,
                    fila.f_prescripcion.strftime("%d/%m/%Y"),
                    fila.medicamento_1,
                    fila.medicamento_2,
                    fila.medico))
   
    def actualizar_prescripcion(self,receta: tuple, tv):
        """
            Actualiza la información de una receta médica existente.
        
            :param receta: (0= medico, 1=cal_fec_pre, 2=paciente, 3=cal_fec_nac, 4=edad,
                        5=cobertura, 6=diagnostico, 7=medicamento_1, 8=medicamento_2, 9=rec_med_id)
	    """
        msg_error = ""
        try:
            medico = receta[0].get().title().strip() 
            self.validar_prescripcion(medico, "medico")

        except Exception as e:
            msg_error += str(e)
            self.log_text(str(e))            

        try:
            paciente = receta[2].get().title().strip()
            self.validar_prescripcion(paciente, "paciente")

        except Exception as e:
            msg_error += str(e)
            self.log_text(str(e))         
        

        if msg_error != "":
            messagebox.showerror(title="Error", message=msg_error)
            print(msg_error)
        else:

            respuesta = messagebox.askokcancel(
                title="Actualización de datos", message="¿Confirma los cambios a realizar?"
            )

            if respuesta == True:
                	
                actualizar =RecetaMedica.update(medico = medico,
                f_prescripcion = receta[1].get_date(),
                nombre_paciente = paciente,
                f_nac_pac = receta[3].get_date(),
                edad = receta[4].get(),
                cobertura = receta[5].get().upper().strip(),
                diagnostico = receta[6].get().title().strip(),
                medicamento_1 = receta[7].get().strip(),
                medicamento_2 = receta[8].get().strip()).where(RecetaMedica.rec_med_id == receta[9].get()) 

                actualizar.execute()               
                
                self.limpiar_campos(receta)

                self.actualizar_treeview(tv)

                messagebox.showinfo(
                    title="Actualización", message="La receta fue actualizada exitosamente"
                )
                return True

    def eliminar_prescripcion(self,tv):
        """
            eliminar_prescripción: elimina la receta que el usuario ha seleccionado en el treeview
        
            :param tv: treeview)
	    """
        valor = tv.selection()
        if len(valor) == 1:
            respuesta = messagebox.askyesno(
                title="Baja de Receta Médica",
                message="¿Confirma que desea eliminar la receta generada?",
            )
            if respuesta == True:
                item = tv.item(valor)              
                mi_id = item["text"]

                elim_receta = RecetaMedica.get(RecetaMedica.rec_med_id == mi_id)
                elim_receta.delete_instance()
                self.actualizar_treeview(tv)
                
                messagebox.showinfo(
                    "Baja de Receta Médica",
                    message="¡Receta Médica eliminada exitosamente!",
                )
            else:
                self.actualizar_treeview(tv)
        else:
            messagebox.showwarning(
                title="Atención", message="¡Debe seleccionar una receta a eliminar!"
            )

    # LIMPIAR FORMULARIO
    def limpiar_campos(self,receta: tuple):
        """
            Limpia los campos del formulario.
        
            :param receta: (0= medico, 1=cal_fec_pre, 2=paciente, 3=cal_fec_nac, 4=edad,
                        5=cobertura, 6=diagnostico, 7=medicamento_1, 8=medicamento_2, 9=rec_med_id)
	    """

        hoy = date.today()
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
    
    def validar_prescripcion(self,dato, campo):
        """
            VALIDACION REGEX: valido que los campos de paciente y médico se completen solo con texto
        
            :param dato: dato ingresado por el usuario del campo a validar
            :param campo: nombre del campo a validar
	    """
        error = ""

        if not re.match("^[A-Za-záéíóú\s]+$", dato):
            error = error + "Error: '"+ dato + "' en el campo " + campo + " no es válido o está vacío. "
            raise Exception(error)

    def calcular_edad(self,f_nac, f_pre):
        """
            CALCULAR LA EDAD DEL PACIENTE: edad del paciente en la fecha en la que se realiza la receta
        
            :param f_nac: fecha de nacimiento del paciente
            :param f_pre: fecha de la prescripción del paciente
	    """

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

    def log_text(self, txt_error:str, trans="[MODIFICACION]"):
        """
            Log de errores: se registra los errores que se ingresaron en los campos de medico y paciente 
        
            :param txt_error: mensaje de error
            :param trans: transacción desde donde se detecta el error
	    """
        try:
            ahora = datetime.now()
            str_ahora = ahora.strftime('%d/%m/%Y %H:%M:%S')                 
            archivo = open('./logs/log_app.txt','w')
            archivo.write(str_ahora + " - " +trans+" "+txt_error+"\n")
            archivo.close()
        except TypeError as te:
            print("Solo se puede pasar un texto!")   

        