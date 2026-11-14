import json
import carga_y_guarda
import validaciones

ARCH_USUARIOS = "usuarios.json"
ARCH_PACIENTES = "pacientes.json"
ARCH_CONSULTAS = "consultas.json"

def registrar_paciente():
    print("Registro de pacientes")
    pacientes = carga_y_guarda.cargar(ARCH_PACIENTES)
    
    identificacion = validaciones.pedir_texto("N° de identidicacion: ")
    
    if validaciones.buscar_por_id(pacientes,identificacion):
        print("Ya existe un paciente con este numero registado")
        return
    pacientes.append({
    "Num_Cedula": identificacion,
    "nombres": validaciones.pedir_nom_y_genero("Nombres: "),
    "apellidos": validaciones.pedir_nom_y_genero("Apellidos: "),
   "telefono": validaciones.pedir_texto("Teléfono: "),
    "email": validaciones.pedir_email("E-mail: "),
    "direccion": validaciones.pedir_texto("Dirección: "),
    "genero": validaciones.pedir_nom_y_genero("Género: "),
   "estado_civil": validaciones.pedir_texto("Estado civil: "),
    })
    carga_y_guarda.guardar(ARCH_PACIENTES,pacientes)
    print("Paciente registrado correctamente.")
    
    
    
def registrar_usuario():
    print("\n--- Registro de usuario ---")
    usuarios = carga_y_guarda.cargar(ARCH_USUARIOS)

    identificacion = validaciones.pedir_texto("No. de identificación: ")
    if validaciones.buscar_por_id(usuarios, identificacion):
        print("Ya existe un usuario con esa identificación.")
        return

    nombres = validaciones.pedir_nom_y_genero("Nombres: ")
    apellidos = validaciones.pedir_nom_y_genero("Apellidos: ")
    telefono = validaciones.pedir_entero("Teléfono: ")
    email = validaciones.pedir_email("E-mail corporativo (será el usuario): ")
    if any(u["email"].lower() == email for u in usuarios):
        print("Ya existe un usuario con ese e-mail.")
        return
    direccion = validaciones.pedir_texto("Dirección: ")
    password = validaciones.crear_contraseña()
    print("Su contraseña es:", password,"¡¡PORFAVOR ANOTARLA!!")

    rol = ""
    while rol not in ("1", "2"):
        rol = input("Rol (1 = médico, 2 = administrativo): ").strip()
    rol = "medico" if rol == "1" else "administrativo"

    usuarios.append({
        "Num_Cedula": identificacion, "nombres": nombres,
        "apellidos": apellidos, "telefono": telefono, "email": email,
        "direccion": direccion, "password": password, "rol": rol,
    })
    carga_y_guarda.guardar(ARCH_USUARIOS, usuarios)
    print("Usuario registrado correctamente.")
    

def crear_admin_inicial():
    if carga_y_guarda.cargar(ARCH_USUARIOS):
        return
    admin = {
        "identificacion": "0000",
        "nombres": "Admin",
        "apellidos": "Administrador",
        "telefono": "555 000111",
        "email": "admin@acmeclinic.com",
        "direccion": "Cl 185 # 26 – 85",
        "password": "Admin123",  
        "rol": "administrativo",
    }
    print("Usuario: admin@acmeclinic.com, Contraseña: Admin123")
    carga_y_guarda.guardar(ARCH_USUARIOS, [admin])
    
def historia_clinica():
    print("\n--- Historia clínica ---")
    paciente = validaciones.buscar_por_id(carga_y_guarda.cargar(ARCH_PACIENTES), validaciones.pedir_texto("Identificación del paciente: "))
    if not paciente:
        print("El paciente no está registrado.")
        return

    print("\n" + "=" * 50)
    print("DATOS DEL PACIENTE")
    print("=" * 50)
    print(f"Identificación: {paciente['Num_Cedula']}")
    print(f"Nombre:         {paciente['nombres']} {paciente['apellidos']}")
    print(f"Teléfono:       {paciente['telefono']}")
    print(f"E-mail:         {paciente['email']}")
    print(f"Dirección:      {paciente['direccion']}")
    print(f"Género:         {paciente['genero']}")
    print(f"Estado civil:   {paciente['estado_civil']}")

    consultas = [c for c in carga_y_guarda.cargar(ARCH_CONSULTAS) if c["paciente_id"] == paciente["Num_Cedula"]]
    validaciones.comprar_fechas(consultas)

    print("\n" + "=" * 50)
    print("HISTORIAL DE CONSULTAS")
    print("=" * 50)
    if not consultas:
        print("El paciente no tiene consultas registradas.")
        return

    for c in consultas:
        print(f"\nFecha:        {c['fecha']}")
        print(f"Médico:       {c['medico_nombre']}")
        print(f"Síntomas:     {', '.join(c['sintomas'])}")
        print(f"Diagnóstico:  {c['diagnostico']}")
        print("Medicamentos:")
        for m in c["prescripciones"]:
            print(f"  - {m['medicamento']} | cantidad: {m['cantidad']} | "
                  f"dosis: {m['dosis_diaria']} | días: {m['dias_tratamiento']}")
        print("-" * 50)