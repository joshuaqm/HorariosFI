from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Define una clase para representar cada fila de datos
class Asignatura:
    def __init__(self, clave, grupo, profesor, tipo, horario, dias, cupo, dificultad):
        self.clave = clave
        self.grupo = grupo
        self.profesor = profesor
        self.tipo = tipo
        self.horario = horario
        self.dias = dias
        self.cupo = cupo
        self.dificultad = dificultad

    def __str__(self):
        return f"Asignatura(clave={self.clave}, grupo={self.grupo}, profesor={self.profesor}, tipo={self.tipo}, horario={self.horario}, dias={self.dias}, cupo={self.cupo}, dificultad={self.dificultad})"

def obtenerDificultad(profesor):
    print(profesor)
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
        
# Base de Datos, Circuitos Electricos, Finanzas, Inteligencia Artificial, Economia
# arreglo_materias = [1644, 1562, 1537, 406, 1413]
arreglo_materias = [1562]
# Configura el servicio de EdgeDriver (suponiendo que msedgedriver esté en el PATH)
driver = webdriver.Edge()

# Abre la página web
driver.get("https://www.ssa.ingenieria.unam.mx/horarios.html")

asignaturas = []  # Lista para almacenar objetos Asignatura

try:
    # Espera a que el formulario esté presente
    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "hrsFormHorarioAsignatura"))
    )

    # Encuentra los elementos del formulario
    clave_input = form.find_element(By.ID, "clave")
    buscar_button = form.find_element(By.ID, "buscar")

    # Llena los campos del formulario
    for clave in arreglo_materias:
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
                    asignatura = Asignatura(cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], dificultad)
                    asignaturas.append(asignatura)
            print(f"Datos obtenidos para la clave de asignatura: {clave}")
        else:
            print(f"No se encontró la clave de asignatura: {clave} en la página de horarios.")
        clave_input.clear()

except Exception as e:
    # En caso de error, captura la excepción y muestra un mensaje
    print("Error al cargar la página:", e)

finally:
    # Cierra el navegador al finalizar
    driver.quit()

# print("Tipos de horario: \n1. Matutino\n2.Vespertino\n")
# tipo_horario = int(input("Ingresa el numero del tipo de horario quieres: "))
# if tipo_horario == 1:
#     print("\nDificultad: \n1. Facil\n2. Medio\n3. Dificil\n")
#     tipo_horario = int(input("Ingresa el numero de dificultad que quieres(escoge en base a tu numero de inscripcion): "))
# elif tipo_horario == 2:
#     print("\nDificultad: \n1. Facil\n2. Medio\n3. Dificil\n")
#     tipo_horario = int(input("Ingresa el numero de dificultad que quieres(escoge en base a tu numero de inscripcion): "))

# Ahora puedes trabajar con la lista de objetos Asignatura según tus necesidades
formatearObjetos(asignaturas)
for asignatura in asignaturas:
    print(asignatura)
