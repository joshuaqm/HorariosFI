from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

materias = int(input("Ingresa el numero de asignaturas a incluir en el horario: "))
arreglo_materias = []
for i in range(materias):
    clave = input("Ingresa la clave de la asignatura " + str(i+1) + ": ")
    arreglo_materias.append(clave)
    print(arreglo_materias)

# Configura el servicio de EdgeDriver (suponiendo que msedgedriver esté en el PATH)
driver = webdriver.Edge()

# Abre la página web
driver.get("https://www.ssa.ingenieria.unam.mx/horarios.html")

try:
    # Espera a que el formulario esté presente
    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "hrsFormHorarioAsignatura"))
    )

    # Encuentra los elementos del formulario
    clave_input = form.find_element(By.ID, "clave")
    buscar_button = form.find_element(By.ID, "buscar")

    # Lista para almacenar los DataFrames de cada tabla encontrada
    data_frames = []

    # Llena los campos del formulario
    for clave in arreglo_materias:
        clave_input.send_keys(clave)
        # Envía el formulario haciendo clic en el botón de búsqueda
        buscar_button.click()
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        # Encuentra la tabla por su clase
        table = soup.find('table', {'class': 'table table-horarios-custom'})
        if table:
            # Procesa la tabla y crea un DataFrame
            rows = table.find_all('tr')
            data = []
            for row in rows:
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                # Verifica si la fila tiene datos válidos
                if cols and len(cols) == 7:  # Asumiendo que cada fila tiene 7 columnas
                    data.append(cols)
            # Crea el DataFrame si hay datos válidos
            if data:
                df = pd.DataFrame(data, columns=['Clave', 'Gpo', 'Profesor', 'Tipo', 'Horario', 'Dias', 'Cupo'])
                data_frames.append(df)
                print(df)
            else:
                print("No se encontró la clave de asignatura: " + clave + " en la página de horarios.")
        else:
            print("No se encontró la clave de asignatura: " + clave + " en la página de horarios.")
        clave_input.clear()

    # Aquí puedes trabajar con los DataFrames como necesites
    # Por ejemplo, concatenar todos los DataFrames en uno solo si es necesario

except Exception as e:
    # En caso de error, captura la excepción y muestra un mensaje
    print("Error al cargar la página:", e)

finally:
    # Cierra el navegador al finalizar
    driver.quit()
