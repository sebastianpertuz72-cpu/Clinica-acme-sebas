import json
import carga_y_guarda
import validaciones

ARCH_USUARIOS = "usuarios.json"
ARCH_PACIENTES = "pacientes.json"
ARCH_CONSULTAS = "consultas.json"

def registrarpaciente():
    print("Registro de pacientes")
    pacientes = carga_y_guarda.cargar(ARCH_PACIENTES)
    
    identificacion = validaciones.pedir_texto("N° de identidicacion: ")
    if validaciones.buscar_por_id(pacientes,identificacion):
        print("Ya existe un paciente con este numero registado")
        return
    pacientes.append({
    "identificacion": identificacion,
    "nombres": validaciones.pedir_texto("Nombres: "),
    "apellidos": validaciones.pedir_texto("Apellidos: "),
   "telefono": validaciones.pedir_texto("Teléfono: "),
    "email": validaciones.pedir_email("E-mail: "),
    "direccion": validaciones.pedir_texto("Dirección: "),
    "genero": validaciones.pedir_texto("Género: "),
   "estado_civil": validaciones.pedir_texto("Estado civil: "),
    })
    carga_y_guarda.guardar(ARCH_PACIENTES,pacientes)
    print("Paciente registrado correctamente.")
    
while True:
    registrarpaciente()