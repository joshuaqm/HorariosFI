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

class Temporal:
    def __init__(self, horario, dias):
        self.horario = horario
        self.dias = dias
    
    def __str__(self):
        return f"Temporal(horario={self.horario}, dias={self.dias})"

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
    """Adds new_horario to arr if it doesn't overlap with existing horarios by day and hour."""
    # Convert the new_horario's start and end times to minutes
    new_start, new_end = map(conversionMinutos, new_horario.horario)
    
    for existing_horario in arr:
        # Check for day overlap
        day_overlap = any(day in new_horario.dias for day in existing_horario.dias)
        if not day_overlap:
            # No day overlap, continue to the next existing_horario
            continue
        
        # Convert the existing_horario's start and end times to minutes
        existing_start, existing_end = map(conversionMinutos, existing_horario.horario)
        
        # Check for time overlap
        if not (new_end <= existing_start or new_start >= existing_end):
            # Overlap detected, do not add new_horario
            return False
    
    # No overlap detected, add new_horario
    arr.append(new_horario)
    return True

def generate_days_dict(arr):
    # Step 1: Initialize the dictionary with days as keys and empty lists as values
    days_dict = {day: [] for day in range(1, 7)}
    
    # Step 2: Iterate over each Horario object in arr
    for horario in arr:
        # Step 3: Iterate over each day in the Horario object's arregloDias
        for day in horario.arregloDias:
            # Step 4: Append the Horario object to the corresponding list in days_dict
            days_dict[day].append(horario.arregloHoras)
    
    # Step 5: Return or print the dictionary
    return days_dict

def generaOpciones(asignaturas_clave_turno):
    n_opciones_base = len(asignaturas_clave_turno[0])
    opcionesFinales = [{i: [] for i in range(1, 7)} for _ in range(n_opciones_base)]
    
    n_total_asignaturas = len(asignaturas_clave_turno)
    # print(n_total_asignaturas)
    # print(opcionesFinales
    #CORREGIR ESTA LOGICA PARA CAMBIAR DE ALMACENAR EN DICCIONARIO A ALMACENAR EN ARREGLOS
# opcionesFinales = [[] for _ in range(n_opciones_base)]
    # for asignatura_clave_turno in asignaturas_clave_turno:
    #     for i, asignatura in enumerate(asignatura_clave_turno):
    #         # Assuming you have a way to determine which opcion an asignatura should be added to
    #         # This is a placeholder logic, replace it with your actual logic
    #         opcion_index = i % n_opciones_base  # Example logic: distribute asignaturas evenly across opciones
    #         opcionesFinales[opcion_index].append(asignatura)  
    for i, opcion in enumerate(opcionesFinales):
        for key in opcion:
            for asignatura in asignaturas_clave_turno[0][i].dias:  # Assuming asignaturas_clave_turno structure matches your needs
                if asignatura == key:
                    # opcionesFinales[i][key].append((asignaturas_clave_turno[0][i].clave,asignaturas_clave_turno[0][i].grupo,asignaturas_clave_turno[0][i].horario))
                    opcionesFinales[i][key].append(asignaturas_clave_turno[0][i])
    
    # To print the options
    for opcion in opcionesFinales:
        print("Opción:" + str(opcionesFinales.index(opcion)+1))
        for key in opcion:
            if opcion[key]:
                print(f"{key}: {opcion[key]}")
            else:
                print(f"{key}: Libre")
        print("\n")

    # print("Se generaron: " + str(len(opcionesFinales)) + " opciones")
    # The first index is the option in opcionesFinales
    # The second index is first key of the day were the object is stored
    # The third index is the object itself
    # After accessing the object, you can access its attributes like this:
    # print((opcionesFinales[0][1][0].dias))
    # print((opcionesFinales[0][1][0].horario))
    # temporal = Temporal(opcionesFinales[0][1][0].horario, opcionesFinales[0][1][0].dias)
    # print(temporal)
    # print((opcionesFinales[0]))
    # print((opcionesFinales[1][2][0].dias))
    # print((opcionesFinales[1][2][0].horario))

    # print((asignaturas_clave_turno))
    # print((asignaturas_clave_turno[1][0]))
    # print((asignaturas_clave_turno[1][1]))
    # print((asignaturas_clave_turno[1][2]))
    
    # for asignatura in asignaturas_clave_turno[1]
       
    
asignaturas = []
asignaturas.append(Asignatura('1644', '4', 'ING. LUCIRALIA HERNANDEZ HERNANDEZ', 'T', ['15:00','17:00'], [1,3,5], 40, 0, 1))
asignaturas.append(Asignatura('1644', '6', 'M.C. DAVID RICARDO RUIZ REYES', 'T', ['17:00','19:00'], [2,3,4], 40, 0, 1))
# asignaturas.append(Asignatura('1644', '8', 'ING. LUCIRALIA FAKE', 'T', ['19:00','21:00'], [1,3,5], 40, 0, 1))
asignaturas.append(Asignatura('1562', '1', 'ING. VICTOR MANUEL SANCHEZ ESQUIVEL', 'T', ['16:00','17:30'], [2,4], 40, 0, 1))
asignaturas.append(Asignatura('1562', '2', 'M.I. PATRICIA HONG CIRION', 'T', ['18:00','19:30'], [2,4], 40, 0, 1))
asignaturas.append(Asignatura('1562', '3', 'ING. IVAN MARTINEZ PEREZ', 'T', ['20:30','22:00'], [2,4], 40, 0, 1))
# asignaturas.append(Asignatura('1537', '2', 'ING. PROFESOR POR ASIGNAR', 'T', ['17:00','20:00'], [5], 40, 0, 1))
# asignaturas.append(Asignatura('1537', '6', 'MTRO. ALFREDO URIBE ARANDA', 'T', ['18:00','21:00'], [5], 40, 0, 1))
asignaturas_separadas = separarAsignaturas(asignaturas, "Vespertino")
generaOpciones(asignaturas_separadas)

