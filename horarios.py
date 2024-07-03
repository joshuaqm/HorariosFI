from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Define una clase para representar cada fila de datos
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

def obtenerDificultad(profesor):
    #print(profesor)
    return 0

def formatearObjetos(asignaturas):
    for asignatura in asignaturas:
        asignatura.profesor = asignatura.profesor.split('(', 1)[0]
        hora_inicio, hora_fin = asignatura.horario.split(' a ')
        asignatura.horario = [hora_inicio, hora_fin]
        dias_numerico = []
        for dia in asignatura.dias.split(','):  # Directly iterate over the split result
            dia = dia.strip()  # Strip spaces from each day
            if dia == 'Lun':
                dias_numerico.append(1)
            elif dia == 'Mar':
                dias_numerico.append(2)
            elif dia == 'Mie':
                dias_numerico.append(3)
            elif dia == 'Jue':
                dias_numerico.append(4)
            elif dia == 'Vie':
                dias_numerico.append(5)
            elif dia == 'Sab':
                dias_numerico.append(6)
        asignatura.dias = dias_numerico
        
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

def imprimirElementos(asignaturas_por_clave_y_turno, turno_elegido):
    for clave, asignaturas in asignaturas_por_clave_y_turno.items():
            print(f"Clave: {clave}")
            print(f"Asignaturas en turno {turno_elegido}:")
            for asignatura in asignaturas[turno_elegido]:
                print(asignatura)
            print()

# print(type(asignaturas_por_clave_y_turno))   DICTIONARY
#     print(type(asignaturas_por_clave_y_turno.items()))  DICTIONARY ITEMS
#     print(type(turno_elegido)) STRING
#     for asingatura in asignaturas_por_clave_y_turno.items():  
#         print(type(asingatura))   TUPLE
#         print(asingatura)    
def generaOpciones(asignaturas_clave_turno):
    opciones = {}
    
    return opciones


# Configura el servicio de EdgeDriver (suponiendo que msedgedriver esté en el PATH)
driver = webdriver.Edge()

# Abre la página web
driver.get("https://www.ssa.ingenieria.unam.mx/horarios.html")

asignaturas = []  # Lista para almacenar objetos Asignatura

def obtenerDatos(arreglo_materias):
    try:
        # Espera a que el formulario esté presente
        form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "hrsFormHorarioAsignatura"))
        )

        # Encuentra los elementos del formulario
        clave_input = form.find_element(By.ID, "clave")
        buscar_button = form.find_element(By.ID, "buscar")

        prioridad = 0
        # Llena los campos del formulario
        for clave in arreglo_materias:
            prioridad += 1
            clave_input.send_keys(str(clave))  # Asegúrate de enviar la clave como string
            # Envía el formulario haciendo clic en el botón de búsqueda
            buscar_button.click()
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            # Encuentra la tabla por su clase
            table = soup.find('table', {'class': 'table table-horarios-custom'})
            if table:
                # Procesa la tabla y crea un DataFrame
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    cols = [col.text.strip() for col in cols]
                    # Verifica si la fila tiene datos válidos
                    if cols and len(cols) == 7:  # Asumiendo que cada fila tiene 7 columnas
                        # Crea un objeto Asignatura y agrégalo a la lista
                        profesor = cols[2].split('(', 1)[0]
                        dificultad = obtenerDificultad(profesor)
                        asignatura = Asignatura(cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], dificultad, prioridad)
                        asignaturas.append(asignatura)
                print(f"Datos obtenidos para la clave de asignatura: {clave}")
            else:
                print(f"No se encontró la clave de asignatura: {clave} en la página de horarios.")
            clave_input.clear()
        return asignaturas
    except Exception as e:
        # En caso de error, captura la excepción y muestra un mensaje
        print("Error al cargar la página:", e)

    finally:
        # Cierra el navegador al finalizar
        driver.quit()

def main():
    # Base de Datos, Circuitos Electricos, Finanzas, Inteligencia Artificial, Economia
    # arreglo_materias = [1644, 1562, 1537, 406, 1413]
    arreglo_materias = [1644, 1562]
    # Ejecutamos las peticiones al navegador
    asignaturas = obtenerDatos(arreglo_materias)
    #Le damos formato de arreglo al horario y dias
    formatearObjetos(asignaturas)
    # print("Tipos de horario: \n1. Matutino\n2.Vespertino\n")
    # tipo_horario = int(input("Ingresa el numero del turno de horario quieres: "))
    tipo_horario = 2
    if tipo_horario == 1:
        turno_elegido = "Matutino"
    #     print("\nDificultad: \n1. Facil\n2. Medio\n3. Dificil\n")
    #     tipo_horario = int(input("Ingresa el numero de dificultad que quieres(escoge en base a tu numero de inscripcion): "))
    elif tipo_horario == 2:
        turno_elegido = "Vespertino"

    # Separamos las asignaturas por clave y turno
    asignaturas_clave_turno = separarAsignaturas(asignaturas, turno_elegido)
    # for objeto in asignaturas_clave_turno:
    #     for asignatura in objeto:
    #         print(asignatura)     
    print(asignaturas_clave_turno[1][0])   
    #imprimirElementos(asignaturas_por_clave_y_turno, turno_elegido)
    grupos = generaOpciones(asignaturas_clave_turno)
    #     print("\nDificultad: \n1. Facil\n2. Medio\n3. Dificil\n")
    #     tipo_horario = int(input("Ingresa el numero de dificultad que quieres(escoge en base a tu numero de inscripcion): "))
    print("Opciones disponibles: ")

    # Separamos las asignaturas por clave y turno
    # Tu lista de objetos asignatura

main()