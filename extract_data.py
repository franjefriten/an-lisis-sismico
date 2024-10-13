import requests
import bs4 as bs
import pandas as pd
from datetime import datetime
import os, sys

DOMINIO = r"https://www.ign.es/web/ign/portal/sis-catalogo-terremotos/-/catalogo-terremotos/"

def try_parsing_date(text):
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

def get_last_earthquakes():
    URL = r'https://www.ign.es/web/ign/portal/ultimos-terremotos/-/ultimos-terremotos/'
    respuesta = requests.get(URL)

    contenido = bs.BeautifulSoup(respuesta.content, 'html.parser')
    tabla = contenido.find('table', class_=None)

    filas = tabla.tbody.find_all_next('tr')

    columnas = []
    columnas_html = filas[0].find_all('th')
    print(columnas_html)
    for col in columnas_html:
        if col.string != None:
            columnas.append(col.string)
        if col.string == None and col.a == None:
            columnas.append(col.contents[0])
        if col.string == None and col.a != None:
            columnas.append(col.a.contents[0])

    df = pd.DataFrame(
        columns=columnas
    )

    index = 0
    for fila in filas[1:]:
        datos = fila.find_all('td')
        for dato, col in zip(datos, columnas):
            df.loc[index, col] = dato.string
        index += 1
    
    return df


def get_last_ten_earthquakes():

    URL = r'https://www.ign.es/web/ign/portal/ultimos-terremotos/-/ultimos-terremotos/get10dias?_IGNGFSSismoSismicidadReciente_WAR_IGNGFSSismoSismicidadRecienteportlet_formDate=1728763945657&_IGNGFSSismoSismicidadReciente_WAR_IGNGFSSismoSismicidadRecienteportlet_dias=10'
    respuesta = requests.get(URL)

    contenido = bs.BeautifulSoup(respuesta.content, 'html.parser')
    tabla = contenido.find('table', class_=None)

    filas = tabla.tbody.find_all_next('tr')

    columnas = []
    columnas_html = filas[0].find_all('th')
    print(columnas_html)
    for col in columnas_html:
        if col.string != None:
            columnas.append(col.string)
        if col.string == None and col.a == None:
            columnas.append(col.contents[0])
        if col.string == None and col.a != None:
            columnas.append(col.a.contents[0])

    df = pd.DataFrame(
        columns=columnas
    )

    index = 0
    for fila in filas[1:]:
        datos = fila.find_all('td')
        for dato, col in zip(datos, columnas):
            df.loc[index, col] = dato.string
        index += 1
    
    return df


def get_last_month_felt_earthquakes():

    URL = r'https://www.ign.es/web/ign/portal/ultimos-terremotos/-/ultimos-terremotos/get30dias'
    respuesta = requests.get(URL)

    contenido = bs.BeautifulSoup(respuesta.content, 'html.parser')
    tabla = contenido.find('table', class_=None)

    filas = tabla.tbody.find_all_next('tr')

    columnas = []
    columnas_html = filas[0].find_all('th')
    print(columnas_html)
    for col in columnas_html:
        if col.string != None:
            columnas.append(col.string)
        if col.string == None and col.a == None:
            columnas.append(col.contents[0])
        if col.string == None and col.a != None:
            columnas.append(col.a.contents[0])

    df = pd.DataFrame(
        columns=columnas
    )

    index = 0
    for fila in filas[1:]:
        datos = fila.find_all('td')
        for dato, col in zip(datos, columnas):
            df.loc[index, col] = dato.string
        index += 1
    
    return df
    
def get_earthquakes(
        latMin: float,
        latMax: float,
        longMin: float,
        longMax: float,
        startDate: str,
        endDate: str,
        intMin: float = -1,
        intMax: float = -1,
        magMin: float = -1,
        magMax: float = -1,
        profMin: float = -1,
        profMax: float = -1,
        cond: str = ''    
):

    if intMin == -1 or intMax == -1:
        selIntensidad = 'N'
        intMin = ''
        intMax = ''
    else:
        selIntensidad = 'Y'

    if magMin == -1 or magMax == -1:
        selMagnitud = 'N'
        magMin = ''
        magMax = ''
    else:
        selMagnitud = 'Y'

    if profMin == -1 or profMax == -1:
        selProf = 'N'
        profMin = ''
        profMax = ''
    else:
        selProf = 'Y'

    indice = 50

    query = "searchTerremoto?"
    query = ''.join([query, 'latMin=', str(latMin), '&'])
    query = ''.join([query, 'latMax=', str(latMax), '&'])
    query = ''.join([query, 'longMin=', str(longMin), '&'])
    query = ''.join([query, 'longMax=', str(longMax), '&'])
    query = ''.join([query, 'startDate=', startDate, '&'])
    query = ''.join([query, 'endDate=', endDate, '&'])
    query = ''.join([query, 'selIntensidad=', selIntensidad, '&'])
    query = ''.join([query, 'selMagnitud=', selMagnitud, '&'])
    query = ''.join([query, 'intMin=', str(intMin), '&'])
    query = ''.join([query, 'intMax=', str(intMax), '&'])
    query = ''.join([query, 'magMin=', str(magMin), '&'])
    query = ''.join([query, 'magMax=', str(magMax), '&'])
    query = ''.join([query, 'selProf=', selProf, '&'])
    query = ''.join([query, 'profMin=', str(profMin), '&'])
    query = ''.join([query, 'profMax=', str(profMax), '&'])
    query = ''.join([query, 'cond=', cond, '&'])    
    query_index = ''.join([query, 'indice=', str(indice)])
    URL = os.path.join(DOMINIO, query_index)
    
    respuesta = requests.get(URL)
    contenido = bs.BeautifulSoup(respuesta.content, 'html.parser')
    tabla = contenido.find('table', class_=None)
    filas = tabla.tbody.find_all_next('tr')
    columnas = []
    columnas_html = filas[0].find_all('th')

    for col in columnas_html:
        if col.string != None:
            columnas.append(str(col.string))
        if col.string == None and col.a == None:
            columnas.append(str(col.contents[0]))
        if col.string == None and col.a != None:
            columnas.append(str(col.a.contents[0]))

    df = pd.DataFrame(
        columns=columnas,
    )
    df = df.drop('Más Info', axis=1)
    columnas.pop(-1)

    index = 0
    for fila in filas[1:]:
        datos = fila.find_all('td')
        for dato, col in zip(datos, columnas):
            df.loc[index, col] = str(dato.string)
        index += 1

    indice += 50
    query_index = ''.join([query, 'indice=', str(indice)])
    URL = os.path.join(DOMINIO, query_index)
    respuesta = requests.get(URL)
    contenido = bs.BeautifulSoup(respuesta.content, 'html.parser')
    tabla = contenido.find('table', class_=None)

    while len(tabla.find_all('tr')) > 1:
        index = indice
        for fila in filas[1:]:
            datos = fila.find_all('td')
            for dato, col in zip(datos, columnas):
                if dato.string is not None:
                    df.loc[index, col] = str(dato.string)
            index += 1
    
        indice += 50
        query_index = ''.join([query, 'indice=', str(indice)])
        URL = os.path.join(DOMINIO, query_index)
        respuesta = requests.get(URL)
        contenido = bs.BeautifulSoup(respuesta.content, 'html.parser')
        tabla = contenido.find('table', class_=None)
    
    num_cols = ['Latitud', 'Longitud', 'Profundidad', 'Magnitud', 'Int. max.']
    df = df.astype(dict(zip(num_cols, 5*['float'])))
    df = df.astype({"Fecha": 'str', "Hora UTC": 'str', "Hora Local": 'str', "Tipo Mag.": 'str', "Localización": 'str'})
    df.Fecha = pd.to_datetime(df.Fecha, format="%d/%m/%Y")
    df['Hora UTC'] = pd.to_datetime(df['Hora UTC'], format="%H:%M:%S")
    df['Hora Local'] = pd.to_datetime(df['Hora Local'], format="%H:%M:%S")
    df['Year'] = df['Fecha'].dt.year
    #print(URL)
    return df


if __name__ == "__main__":
    df = get_earthquakes(
        latMin=26,
        latMax=45,
        longMin=-20,
        longMax=6,
        startDate="01/01/2024",
        endDate="12/10/2024",
        intMin=1,
        intMax=3
    )

