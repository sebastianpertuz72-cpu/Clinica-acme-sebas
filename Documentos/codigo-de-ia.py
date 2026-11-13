

"""Sistema de diagnósticos - Clínica ACME
Usa únicamente la librería estándar json.
"""
import json

ARCH_USUARIOS = "usuarios.json"
ARCH_PACIENTES = "pacientes.json"
ARCH_CONSULTAS = "consultas.json"


# ---------------------------------------------------------------- persistencia
def cargar(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return [ ]


def guardar(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def crear_admin_inicial():
    if cargar(ARCH_USUARIOS):
        return
    admin = {
        "identificacion": "0000",
        "nombres": "Admin",
        "apellidos": "Administrador",
        "telefono": "555 000111",
        "email": "admin@acmeclinic.com",
        "direccion": "Cl 185 # 26 – 85",
        "password": "Admin123",  # contraseña inicial (cámbiala si lo exige tu profesor)
        "rol": "administrativo",
    }
    guardar(ARCH_USUARIOS, [admin])


# ----------------------------------------------------------------- validaciones
def pedir_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  Este campo no puede estar vacío.")


def pedir_email(mensaje):
    while True:
        valor = pedir_texto(mensaje)
        if "@" in valor and "." in valor.split("@")[-1]:
            return valor.lower()
        print("  E-mail no válido.")


def pedir_entero(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit() and int(valor) > 0:
            return int(valor)
        print("  Escribe un número entero mayor que cero.")


def pedir_fecha(mensaje):
    while True:
        valor = input(mensaje).strip()
        partes = valor.split("-")
        if (len(partes) == 3 and all(x.isdigit() for x in partes)
                and len(partes[0]) == 4 and len(partes[1]) == 2 and len(partes[2]) == 2
                and 1 <= int(partes[1]) <= 12 and 1 <= int(partes[2]) <= 31):
            return valor
        print("  Formato inválido. Usa AAAA-MM-DD (ej. 2026-11-11).")


def buscar_por_id(lista, identificacion):
    for item in lista:
        if item["identificacion"] == identificacion:
            return item
    return None


# --------------------------------------------------------------------- login
def login():
    print("=== CLÍNICA ACME - Inicio de sesión ===")
    for _ in range(3):
        email = input("Usuario (e-mail): ").strip().lower()
        password = input("Contraseña: ")
        for u in cargar(ARCH_USUARIOS):
            if u["email"].lower() == email and u["password"] == password:
                print(f"\nBienvenido, {u['nombres']} {u['apellidos']} ({u['rol']})")
                return u
        print("Credenciales incorrectas.\n")
    print("Demasiados intentos fallidos.")
    return None


# ----------------------------------------------------------- registro usuarios
def registrar_usuario():
    print("\n--- Registro de usuario ---")
    usuarios = cargar(ARCH_USUARIOS)

    identificacion = pedir_texto("No. de identificación: ")
    if buscar_por_id(usuarios, identificacion):
        print("Ya existe un usuario con esa identificación.")
        return

    nombres = pedir_texto("Nombres: ")
    apellidos = pedir_texto("Apellidos: ")
    telefono = pedir_texto("Teléfono: ")
    email = pedir_email("E-mail corporativo (será el usuario): ")
    if any(u["email"].lower() == email for u in usuarios):
        print("Ya existe un usuario con ese e-mail.")
        return
    direccion = pedir_texto("Dirección: ")
    password = pedir_texto("Contraseña: ")

    rol = ""
    while rol not in ("1", "2"):
        rol = input("Rol (1 = médico, 2 = administrativo): ").strip()
    rol = "medico" if rol == "1" else "administrativo"

    usuarios.append({
        "identificacion": identificacion, "nombres": nombres,
        "apellidos": apellidos, "telefono": telefono, "email": email,
        "direccion": direccion, "password": password, "rol": rol,
    })
    guardar(ARCH_USUARIOS, usuarios)
    print("Usuario registrado correctamente.")


# ----------------------------------------------------------- registro pacientes
def registrar_paciente():
    print("\n--- Registro de paciente ---")
    pacientes = cargar(ARCH_PACIENTES)

    identificacion = pedir_texto("No. de identificación: ")
    if buscar_por_id(pacientes, identificacion):
        print("Ya existe un paciente con esa identificación.")
        return

    pacientes.append({
        "identificacion": identificacion,
        "nombres": pedir_texto("Nombres: "),
        "apellidos": pedir_texto("Apellidos: "),
        "telefono": pedir_texto("Teléfono: "),
        "email": pedir_email("E-mail: "),
        "direccion": pedir_texto("Dirección: "),
        "genero": pedir_texto("Género: "),
        "estado_civil": pedir_texto("Estado civil: "),
    })
    guardar(ARCH_PACIENTES, pacientes)
    print("Paciente registrado correctamente.")


# ------------------------------------------------------------------ diagnóstico
def diagnosticar(medico):
    print("\n--- Diagnosticar paciente ---")
    if medico["rol"] != "medico":
        print("Solo los usuarios con rol médico pueden diagnosticar.")
        return

    paciente = buscar_por_id(cargar(ARCH_PACIENTES), pedir_texto("Identificación del paciente: "))
    if not paciente:
        print("El paciente no está registrado. Regístralo primero.")
        return
    print(f"Paciente: {paciente['nombres']} {paciente['apellidos']}")

    fecha = pedir_fecha("Fecha de la consulta (AAAA-MM-DD): ")

    print("\nSíntomas (deja vacío y pulsa Enter para terminar):")
    sintomas = []
    while True:
        s = input(f"  Síntoma {len(sintomas) + 1}: ").strip()
        if not s:
            if sintomas:
                break
            print("  Registra al menos un síntoma.")
            continue
        sintomas.append(s)

    diagnostico = pedir_texto("\nDiagnóstico (patología o enfermedad): ")

    print("\nPrescripción médica:")
    prescripciones = []
    while True:
        print(f"  Medicamento {len(prescripciones) + 1}")
        prescripciones.append({
            "medicamento": pedir_texto("    Medicamento: "),
            "cantidad": pedir_entero("    Cantidad: "),
            "dosis_diaria": pedir_texto("    Dosis (cuánto tomar al día): "),
            "dias_tratamiento": pedir_entero("    Tiempo de aplicación (días): "),
        })
        if input("  ¿Agregar otro medicamento? (s/n): ").strip().lower() != "s":
            break

    consultas = cargar(ARCH_CONSULTAS)
    consulta = {
        "fecha": fecha,
        "paciente_id": paciente["identificacion"],
        "medico_id": medico["identificacion"],
        "medico_nombre": f"{medico['nombres']} {medico['apellidos']}",
        "sintomas": sintomas,
        "diagnostico": diagnostico,
        "prescripciones": prescripciones,
    }
    consultas.append(consulta)
    guardar(ARCH_CONSULTAS, consultas)

    # Prescripción médica en su propio JSON (fecha + paciente + médico)
    nombre_archivo = f"prescripcion_{paciente['identificacion']}_{fecha}_{len(consultas)}.json"
    guardar(nombre_archivo, consulta)
    print(f"\nConsulta guardada. Prescripción generada en: {nombre_archivo}")


# --------------------------------------------------------------- historia clínica
def historia_clinica():
    print("\n--- Historia clínica ---")
    paciente = buscar_por_id(cargar(ARCH_PACIENTES), pedir_texto("Identificación del paciente: "))
    if not paciente:
        print("El paciente no está registrado.")
        return

    print("\n" + "=" * 50)
    print("DATOS DEL PACIENTE")
    print("=" * 50)
    print(f"Identificación: {paciente['identificacion']}")
    print(f"Nombre:         {paciente['nombres']} {paciente['apellidos']}")
    print(f"Teléfono:       {paciente['telefono']}")
    print(f"E-mail:         {paciente['email']}")
    print(f"Dirección:      {paciente['direccion']}")
    print(f"Género:         {paciente['genero']}")
    print(f"Estado civil:   {paciente['estado_civil']}")

    consultas = [c for c in cargar(ARCH_CONSULTAS) if c["paciente_id"] == paciente["identificacion"]]
    consultas.sort(key=lambda c: c["fecha"])

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


# ------------------------------------------------------------------------ menú
def menu(usuario):
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registrar usuario")
        print("2. Registrar paciente")
        print("3. Diagnosticar paciente")
        print("4. Historia clínica")
        print("0. Salir")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            registrar_paciente()
        elif opcion == "3":
            diagnosticar(usuario)
        elif opcion == "4":
            historia_clinica()
        elif opcion == "0":
            print("Hasta pronto.")
            break
        else:
            print("Opción no válida.")


def main():
    crear_admin_inicial()
    usuario = login()
    if usuario:
        menu(usuario)


if __name__ == "__main__":
    main()

