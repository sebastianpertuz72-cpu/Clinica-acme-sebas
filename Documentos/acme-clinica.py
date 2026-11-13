import json
import carga_y_guarda
import registros

ruta = "/home/camper/Documentos/"
pacientes_arch = ruta + "pacientes.json"

pacientes = [
    {"Num_Cedula": "1005185919","Nombres":"Sebastian","Apellidos":"Pertuz Sampayo","Num_Telefono":"3215798653","E_Mail":"papas@gmail.com","Direccion":"Cra 34f #55-50","Genero":"Si","Estado_Civil":"Soltero"}
]


with open(pacientes_arch,"w", encoding="utf-8") as listapacientes:
    json.dump(pacientes,listapacientes, indent=4)