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

# def agregaNoTraslapados(arr, new_horario, opcionesFinales):
#     """Adds new_horario to arr if it doesn't overlap with existing horarios by day and hour."""
#     # Convert the new_horario's start and end times to minutes
#     new_start, new_end = map(conversionMinutos, new_horario.horario)
    
#     for existing_horario in arr:
#         # Check for day overlap
#         day_overlap = any(day in new_horario.dias for day in existing_horario.dias)
#         if not day_overlap:
#             # No day overlap, continue to the next existing_horario
#             continue
        
#         # Convert the existing_horario's start and end times to minutes
#         existing_start, existing_end = map(conversionMinutos, existing_horario.horario)
        
#         # Check for time overlap
#         if not (new_end <= existing_start or new_start >= existing_end):
#             # Overlap detected, do not add new_horario
#             return False
    
#     # No overlap detected, add new_horario
#     print(arr[0])
#     arr.append(new_horario)
#     return True
def agregaNoTraslapados(arr, new_horario, opcionesFinales):
    """Adds new_horario to arr if it doesn't overlap with existing horarios by day, hour, and unique clave."""
    # Convert the new_horario's start and end times to minutes
    new_start, new_end = map(conversionMinutos, new_horario.horario)
    
    claveExists = False
    for existing_horario in arr:
        # Check if the clave already exists
        if new_horario.clave == existing_horario.clave:
            claveExists = True
            # Assuming opcionesFinales is to be used here as per the requirement
            # if not opcionesFinales:
            #     opcionesFinales = []
            # opcionesFinales.append(existing_horario)
            # opcionesFinales.append(new_horario)
            break  # Assuming we only care about the first match

    if claveExists:
        # Clave already exists, so we've handled it by creating/updating opcionesFinales
        return False  # Or handle as needed

    for existing_horario in arr:
        # Check for day overlap
        day_overlap = any(day in new_horario.dias for day in existing_horario.dias)
        if not day_overlap:
            continue
        
        # Convert the existing_horario's start and end times to minutes
        existing_start, existing_end = map(conversionMinutos, existing_horario.horario)
        
        # Check for time overlap
        if not (new_end <= existing_start or new_start >= existing_end):
            return False
    
    arr.append(new_horario)
    opcionesFinales.append(arr)
    return True

def generate_days_dict(arr):
    # Step 1: Initialize the dictionary with days as keys and empty lists as values
    days_dict = {day: [] for day in range(1, 7)}
    
    # Step 2: Iterate over each Horario object in arr
    for horario in arr:
        # Step 3: Iterate over each day in the Horario object's arregloDias
        for day in horario.dias:
            # Step 4: Append the Horario object to the corresponding list in days_dict
            days_dict[day].append(horario.horario)
    
    # Step 5: Return or print the dictionary
    return days_dict

def creaArreglo(arreglo, nuevaOpcion, opcionesFinales):
    # Check if arreglo has at least 2 elements and if nuevaOpcion has the attribute 'clave'
    if len(arreglo) > 1 and hasattr(nuevaOpcion, 'clave'):
        # Find the index of the element with the same clave as nuevaOpcion, if it exists
        index = next((i for i, item in enumerate(arreglo) if hasattr(item, 'clave') and item.clave == nuevaOpcion.clave), None)
        if index is not None:
            # If found, delete the element at the found index and append nuevaOpcion
            del arreglo[index]
            arreglo.append(nuevaOpcion)
        else:
            # print("No existe")
            print()
    else:
        # If arreglo does not have enough elements or nuevaOpcion does not have 'clave', print "No existe"
        # print("No existe")
        print()
    
    # Copy arreglo to nuevoArreglo and append it to opcionesFinales
    nuevoArreglo = arreglo.copy()
    opcionesFinales.append(nuevoArreglo)
    
    # Remove the last element from arreglo if it's not empty
    if arreglo:
        arreglo.pop()

def generaOpciones(asignaturas_clave_turno):
    opcionesFinales = []
    n_opciones_base = len(asignaturas_clave_turno[0])
    opciones_base = [[] for _ in range(n_opciones_base)]
    opciones_adicionales = [[] for _ in range(n_opciones_base)]

    for asignaturas in asignaturas_clave_turno:
        for i, asignatura in enumerate(asignaturas):
            # Dynamically extend opciones_base and opciones_adicionales if needed
            while len(opciones_base) <= i:
                opciones_base.append([])
            while len(opciones_adicionales) <= i:
                opciones_adicionales.append([])

            # Now proceed with the original logic, as opciones_base and opciones_adicionales
            # are guaranteed to have a sub-list at index i
            if asignatura not in opciones_base[i]:
                if asignaturas_clave_turno.index(asignaturas) == 0:
                    opciones_base[i].append(asignatura)
                else:
                    opciones_adicionales[i].append(asignatura)
    
    i = 0
    while i < len(opciones_base):
        if(len(opciones_base[i])==0):
            opciones_base.remove(opciones_base[i])
        i+=1
    
    # print(opciones_base)
    print(opciones_adicionales[0][1])
    # print(opciones_base[1][0])
    

    # # Agregar asignaturas no traslapadas a la opcion 1
    # Automating the process with loops
    i = j = k = 0
    while i < len(opciones_base):
        # print(opciones_base[i])
        i+=1

    # Print the number of final options generated
    # print("Se generaron:" + str(len(opcionesFinales)) + " opciones finales")
    # print(opcionesFinales)

    # # Generate and print day dictionaries for each final option
    # for index, opcionFinal in enumerate(opcionesFinales):
    #     opcion_dict = generate_days_dict(opcionFinal)
    #     print(f"Opcion {index + 1}:")
    #     print(opcion_dict)
  
       
    
asignaturas = []
asignaturas.append(Asignatura('1644', '4', 'ING. LUCIRALIA HERNANDEZ HERNANDEZ', 'T', ['15:00','17:00'], [1,3,5], 40, 0, 1))
asignaturas.append(Asignatura('1644', '6', 'M.C. DAVID RICARDO RUIZ REYES', 'T', ['17:00','19:00'], [2,3,4], 40, 0, 1))
asignaturas.append(Asignatura('1644', '8', 'ING. LUCIRALIA FAKE', 'T', ['19:00','21:00'], [1,3,5], 40, 0, 1))
asignaturas.append(Asignatura('1562', '1', 'ING. VICTOR MANUEL SANCHEZ ESQUIVEL', 'T', ['16:00','17:30'], [2,4], 40, 0, 1))
asignaturas.append(Asignatura('1562', '2', 'M.I. PATRICIA HONG CIRION', 'T', ['18:00','19:30'], [2,4], 40, 0, 1))
asignaturas.append(Asignatura('1562', '3', 'ING. IVAN MARTINEZ PEREZ', 'T', ['20:30','22:00'], [2,4], 40, 0, 1))
asignaturas.append(Asignatura('1562', '4', 'ING. IVAN FAKE PEREZ', 'T', ['20:30','22:00'], [2,4], 40, 0, 1))

asignaturas.append(Asignatura('1537', '2', 'ING. PROFESOR POR ASIGNAR', 'T', ['17:00','20:00'], [5], 40, 0, 1))
asignaturas.append(Asignatura('1537', '6', 'MTRO. ALFREDO URIBE ARANDA', 'T', ['18:00','21:00'], [5], 40, 0, 1))
asignaturas_separadas = separarAsignaturas(asignaturas, "Vespertino")
generaOpciones(asignaturas_separadas)

