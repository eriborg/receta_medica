import sqlite3 
from peewee import *

# ##############################################
# MODELO
# ##############################################
# Crear una instancia de Base de datos
db = SqliteDatabase("receta_medica.db")

class BaseModel(Model):
    class Meta:
        database = db    

class RecetaMedica(BaseModel):
    """
        Modelo ORM de Receta Médica.
        
        :param BaseModel: RecetaMedica hereda de BaseModel
	"""
    rec_med_id = AutoField()
    medico = CharField()
    f_prescripcion = DateField()
    nombre_paciente = CharField()
    f_nac_pac = DateField()
    edad = IntegerField()
    cobertura = CharField()
    diagnostico = CharField()
    medicamento_1 = CharField()
    medicamento_2 = CharField()

db.connect()
db.create_tables([RecetaMedica])

