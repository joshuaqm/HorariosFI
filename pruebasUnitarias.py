class Asignatura:
    def __init__(self, clave, grupo, profesor, tipo, horario, dias, cupo, dificultad, prioridad):
        self.clave = clave
        self.grupo = grupo
        self.profesor = profesor
        self.tipo = tipo
        self.horario = horario
        self.dias = dias
        self.cupo = cupo
        self.dificultad = dificultad
        self.prioridad = prioridad
    
    def __str__(self):
        return f"Asignatura(clave={self.clave}, grupo={self.grupo}, profesor={self.profesor}, tipo={self.tipo}, horario={self.horario}, dias={self.dias}, cupo={self.cupo}, dificultad={self.dificultad}, prioridad={self.prioridad})"

def separarAsignaturas(asignaturas, turno):
    asignaturas_turno = []
    asignaturas_por_clave = {}  # Step 2: Use a dictionary to group by clave

    # Existing logic to filter asignaturas by turno
    if turno == "Matutino":
        for asignatura in asignaturas:
            if asignatura.horario[0] <= '13:00':
                asignaturas_turno.append(asignatura)
    elif turno == "Vespertino":
        for asignatura in asignaturas:
            if asignatura.horario[0] > '13:00':
                asignaturas_turno.append(asignatura)

    # Group asignaturas by clave
    for asignatura in asignaturas_turno:
        clave = asignatura.clave
        if clave not in asignaturas_por_clave:
            asignaturas_por_clave[clave] = [asignatura]
        else:
            asignaturas_por_clave[clave].append(asignatura)

    # Convert the dictionary values to an array of arrays
    asignaturas_clave_turno = list(asignaturas_por_clave.values())

    return asignaturas_clave_turno

def conversionMinutos(time_str):
    """Converts a time string HH:MM to minutes, with input validation."""
    if ':' not in time_str:
        print(f"Invalid time format: {time_str}. Expected format: HH:MM.")
        return None
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def agregaNoTraslapados(arr, new_horario):
    """Adds new_horario to arr if it doesn't overlap with existing horarios."""
    new_start, new_end = map(conversionMinutos, new_horario)
    for existing_horario in arr:
        if len(existing_horario) != 2:
            print(f"Invalid horario format: {existing_horario}. Expected format: ['HH:MM', 'HH:MM'].")
            continue
        existing_start, existing_end = map(conversionMinutos, existing_horario)
        # Check for overlap
        if not (new_end <= existing_start or new_start >= existing_end):
            # Overlap detected, do not add new_horario
            return False
    # No overlap detected, add new_horario
    arr.append(new_horario)
    return True

def generaOpciones(asignaturas_clave_turno):
    n_opciones_base = len(asignaturas_clave_turno[0])
    opcionesFinales = [{i: [] for i in range(1, 7)} for _ in range(n_opciones_base)]
    
    n_total_asignaturas = len(asignaturas_clave_turno)
    # print(n_total_asignaturas)
    # print(opcionesFinales

    for i, opcion in enumerate(opcionesFinales):
        for key in opcion:
            for asignatura in asignaturas_clave_turno[0][i].dias:  # Assuming asignaturas_clave_turno structure matches your needs
                if asignatura == key:
                    opcionesFinales[i][key].append((asignaturas_clave_turno[0][i].clave,asignaturas_clave_turno[0][i].grupo,asignaturas_clave_turno[0][i].horario))

       
            
    for opcion in opcionesFinales:
        print("Opción:" + str(opcionesFinales.index(opcion)+1))
        for key in opcion:
            if opcion[key]:
                print(f"{key}: {opcion[key]}")
            else:
                print(f"{key}: Libre")
        print("\n")
    # for asignaturas in asignaturas_clave_turno:
    #     for asignatura in asignaturas:
    #         for dia in asignatura.dias:
    #             horarioNoTraslapado = True
    #             for opcion in opcionesFinales[dia]:
    #                 print("aaaaaaaa"+str(asignatura.horario))
    #                 if not agregaNoTraslapados(opcion, asignatura.horario):
    #                     horarioNoTraslapado = False
    #                     break
    #             if horarioNoTraslapado:
    #                 opcionesFinales[dia].append(asignatura.horario)

    # for dia, horarios in opcionesFinales.items():
    #     if horarios:
    #         for horario in horarios:
    #             print(f"{dia}: {horario}")
    #     else:
    #         print(f"{dia}: Libre")


# Assuming agregaNoTraslapados function checks if the new schedule overlaps with the existing schedules and returns True if it does not overlap.

    print("Se generaron: " + str(len(opcionesFinales)) + " opciones")

    # for opcion in opcionesFinales:
    #     print("Opción:" + str(opcionesFinales.index(opcion)+1))
    #     for key in opcion:
    #         if opcion[key] is not None:
    #             print(f"{key}: {opcion[key].horario}")
    #         else:
    #             print(f"{key}: Libre")
    #     print("\n")

asignaturas = []
asignaturas.append(Asignatura('1644', '4', 'ING. LUCIRALIA HERNANDEZ HERNANDEZ', 'T', ['15:00','17:00'], [1,3,5], 40, 0, 1))
asignaturas.append(Asignatura('1644', '6', 'M.C. DAVID RICARDO RUIZ REYES', 'T', ['17:00','19:00'], [2,3,4], 40, 0, 1))
asignaturas.append(Asignatura('1644', '8', 'ING. LUCIRALIA FAKE', 'T', ['19:00','21:00'], [1,3,5], 40, 0, 1))
asignaturas.append(Asignatura('1562', '1', 'ING. VICTOR MANUEL SANCHEZ ESQUIVEL', 'T', ['16:00','17:30'], [2,4], 40, 0, 1))
asignaturas.append(Asignatura('1562', '2', 'M.I. PATRICIA HONG CIRION', 'T', ['18:00','19:30'], [2,4], 40, 0, 1))
asignaturas.append(Asignatura('1562', '3', 'ING. IVAN MARTINEZ PEREZ', 'T', ['20:30','22:00'], [2,4], 40, 0, 1))
# asignaturas.append(Asignatura('1537', '2', 'ING. PROFESOR POR ASIGNAR', 'T', ['17:00','20:00'], [5], 40, 0, 1))
# asignaturas.append(Asignatura('1537', '6', 'MTRO. ALFREDO URIBE ARANDA', 'T', ['18:00','21:00'], [5], 40, 0, 1))
asignaturas_separadas = separarAsignaturas(asignaturas, "Vespertino")
generaOpciones(asignaturas_separadas)
# Example usage
# horario0 = ['13:00', '15:00']
# horario1 = ['15:00', '17:00']
# horario2 = ['17:00', '19:00']
# horario3 = ['14:00', '16:00']
# horario4 = ['16:00', '18:00']

# arr = []

# # agregaNoTraslapados(arr, horario0)
# # agregaNoTraslapados(arr, horario1)
# agregaNoTraslapados(arr, horario2)
# agregaNoTraslapados(arr, horario3)
# agregaNoTraslapados(arr, horario4)

# print(arr)