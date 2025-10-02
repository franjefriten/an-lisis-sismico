# Software para el análisis sísmico de terremotos a lo largo del territorio español

Software de análisis de terremotos y sismos a lo largo de todo el territorio español.

```
.
├── data/
│   └── ...
├── img/
│   └── ...
├── latex_reports/
│   └── ...
├── __init__.py
├── .gitignore
├── create_plots.R
├── extract_data.py
├── generate_latex_report.py
├── LICENSE
├── manage_data.py
├── README.md
└── requirements.txt
```

## create_plots.R

Función para crear un mapa en formato HTML con valores de terremotos en magnitud y profundidad

## extract_data.py

* get_last_earthquakes: obtener los últimos terremotos relevantes
* get_last_ten_earthquakes: obtener los últimos 10 terremotos
* get_last_month_felt_earthquakes: obtener los últimos terremotos del mes actual que se hayan sentido a simple vista
* get_earthquakes: obtener todos los terremotos detectados según ciertos parámetros. El dataset resultante da valores de la fecha, hora, latitud, longitud, magnitud, intenisdad máxima, profundidad y localización del terremoto.
* download_earthquakes: descargar el archivo .csv dispuesto por IGN con todos los parámetros proporcionados

## manage_data.py

### MARCO

El marco es el funcionamiento básico. Permite la carga de datasets locales o la obtención de datos por funciones de extracción. Posteriormente permite los siguientes análisis:

* plot_map: dibujar el mapa sin datos
* plot_map_data: dibujar mapa con todos los puntos de terremotos registrados, el color representa la magnitud y el tamaño la profundidad
* plot_full_map_analysis: dibujar el mapa con datos más:

  * plot de caja y bigotes con la distribución de profundidad por años
  * histograma de la distribución de la magnitud
  * ajuste lineal entre la magnitud y la profundidad
* plot_int_time: dibujar la intensidad a lo largo del tiempo de todos los terremotos
* plot_int_distribution: histograma de la distribución de intensidad máxima
* plot_mag_time: dibujar la magnitud a lo largo del tiempo de todos los terremotos
* plot_mag_distribution: histograma de la distribución de magnitud
* plot_mag_distribution_ritcher_law: distribución de magnitud más ajuste de la Ley de Richter.

### AVISO

Este software emplea los servicios de Catálogo de Terremotos del Institudo Geográfico Nacional (IGN) en ign.es. Todo se encuentra programado conforme a la normativa específicada en su página web (https://www.ign.es/web/ign/portal/politica-datos) y se encuentra bajo licencia CC-BY 4.0.

El objetivo de este trabajo es méramente educativo y con motivos de investigación
