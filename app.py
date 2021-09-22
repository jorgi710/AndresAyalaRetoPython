# hashlib para pasar a sha1
import hashlib
# time para llevar el tiempo de consulta
import time
# flask para hacer las consultas de la api
from flask import Flask, render_template
# request para ejecutar la consulta
import requests
# Para trabajar con archivos json
import json
# Para tener un numero aleatorio
import random
# Se utiliza pandas para guardar los datos de la tabla
import pandas as pd
# Connection para establecer, crear y agregar datos a la base de datos
from ConnectionDB import crear_tabla, crear_conexión, cerrar_db

app = Flask(__name__)

@app.route('/')
def obtenerRegiones():
    # Url de la API
    url = "https://restcountries-v1.p.rapidapi.com/region/africa"

    headers = {
        'x-rapidapi-host': "restcountries-v1.p.rapidapi.com",
        'x-rapidapi-key': "31f24c8f80mshef58adb2eb9464fp18090bjsn89632ca77503"
    }
    # Respuesta a travel del method get
    response = json.loads(requests.request("GET", url, headers=headers).content)
    # Creo las listas vaciás para posterior pasarle los datos
    regions = []
    cityName = []
    Language = []
    times = []
    # Recorro la repuesta obtenida y anexo a regions para establecer mi primer
    # parameters de la tabla
    for country in response:
        if not country["region"] in regions and country["region"]:
            regions.append(country["region"])
    # A partir de regions lo voy recorriendo, realizo las respetivas consultas para el lenguaje, ciudad
    # y llevar le tiempo de la consulta
    for region in regions:
        # Empieza a correr el tiempo
        start_time = time.time()
        # Voy a mi nueva apí a hacer la consulta y respecto a la region obtenida el item 1
        raw_countries = json.loads(requests.get('https://restcountries.eu/rest/v2/region/' + region).content)
        # Creo un numero aleatorio en el rango correcto
        numeroAleatorio = random.randint(0, len(raw_countries) - 1)
        # En mi lista cityName agrego una ciudad de forma aleatoria
        cityName.append(raw_countries[numeroAleatorio]['name'])
        # Para procesar el lenguaje lo encripto de la forma sha1 y luego lo agrego a Language
        Language.append(hashlib.sha1(raw_countries[numeroAleatorio]['languages'][0]['name'].encode()).hexdigest())
        # Finalizo el tiempo
        end_time = time.time()
        # Establezco la diferencia de tiempos y lo agrego a mi lista times
        times.append(end_time - start_time)
    # Se crea el dataframe para guardar los datos de la consulta
    df_tabla = pd.DataFrame({
        "Region": regions,
        "City Name": cityName,
        "Language": Language,
        "Time [ms]": times
    })
    # Mediante la libraries pandas guardar el tiempo total, tiempo promedio, tiempo minim y
    # tiempo maximo en un diccionario llamado tiempos

    tiempos = {'tiempo total': df_tabla['Time [ms]'].sum().round(2),
               'tiempo promedio': df_tabla['Time [ms]'].mean().round(2),
               'tiempo minim': df_tabla['Time [ms]'].min().round(2),
               'tiempo maximo': df_tabla['Time [ms]'].max().round(2)}
    # Pasamos los datos del dataframe a formato html
    table_html = [df_tabla.to_html(index=False, justify='center', classes='table', )]
    # Establecemos la connexion con la base de datos y su respectiva creation
    db = crear_conexión("tiempos.db")
    crear_tabla(db)
    # Se crear el insert para guardar los datos recopilados del tiempo
    db.execute(
        'INSERT INTO tiempos (tiempo_total, tiempo_promedio, tiempo_minimo, tiempo_maximo) VALUES (?, ?, ?, ?)',
        (tiempos['tiempo tota'], tiempos['tiempo promedio'], tiempos['tiempo minim'], tiempos['tiempo maximo'])
    )
    # Un commit para guardar los datos
    db.commit()

    # Convertir a json el dataframe
    df_tabla.to_json(path_or_buf='tiempos.json')

    # Cerramos la base de datos.
    cerrar_db(db)

    return render_template('index.html', tables=table_html, tiempos=tiempos)

if __name__ == '__main__':
    app.run()
