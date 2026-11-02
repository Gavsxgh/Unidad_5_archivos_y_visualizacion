# Documento de analisis

## 1. Origen y qué representa cada archivo

| **Archivo**                    | **Origen**                                                       | **Qué representa**                                                                                                                                                                                                                                                                         | **Tamaño**                    |
|--------------------------------|------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| Aeropuertos_Satena_2026.csv    | Portal Nacional de Datos Abiertos (Datos.gov.co)                 | Catálogo de aeropuertos que atiende Satena: nombre, ciudad, departamento, tipo de operación (nacional/internacional), códigos OACI e IATA, elevación, temperatura y coordenadas. Es un directorio de infraestructura, sin fechas ni series de tiempo.                                      | 57 filas × 12 columnas        |
| Transporte_Aéreo_Comercial.csv | Portal Nacional de Datos Abiertos (Datos.gov.co)                 | Estadística mensual de vuelos comerciales: cada fila es una ruta origen–destino operada por una aerolínea en un mes, con tipo de tráfico (N/I/E), tipo de vuelo, pasajeros y kilos de carga y correo. Cubre enero–diciembre de 2020, 2021 y 2022, 2023, 2024, 2025 hasta agosto del 2026 . | 478.011 filas × 16 columnas   |
| juvenila.txt                   | Biblioteca de dominio público                                    | «Juvenilia; Prosa ligera», de Miguel Cané, en español: prosa literaria del siglo XIX.                                                                                                                                                                                                      | 8.840 líneas, 84.333 palabras |
| sample3.txt                    | Generado aleatoriamente                                          | Texto de relleno en seudo-latín sin significado real.                                                                                                                                                                                                                                      | 21 líneas, 546 palabras       |

### Calidad de los datos (lo que hubo que corregir)

- Transporte_Aéreo_Comercial.csv trae cada línea envuelta en comillas dobles, por lo que una lectura directa produce una sola columna; hubo que limpiarlo antes de analizarlo. Además, el año aparece como «2,020», hay 15 valores de pasajeros vacíos y los nombres se repiten con variantes (BOGOTA / BOGOTÁ, D.C.; AMERICAN / AMERICAN AIRLINES; ESPANA / ESPAÑA).

- Aeropuertos_Satena_2026.csv tiene tildes mal codificadas (por ejemplo «nariÃ±o»), elevación en pies guardada como texto con comas, 20 de 57 temperaturas en 0 (casi seguro «sin dato») y al menos una latitud sospechosa: Barranquilla figura en 1,09° cuando debería rondar 10,9°. Aunque el nombre dice 2026, la vigencia de todas las filas es 2025.

## 2. Estadísticas descriptivas

| **Archivo / columna**          | **Válidos** | **Promedio** | **Mediana** | **Máximo** | **Mínimo** |
|--------------------------------|-------------|--------------|-------------|------------|------------|
| Transporte · Pasajeros         | 159.480     | 470,99       | 9           | 79.817     | 0          |
| Transporte · Carga/correo (kg) | 159.495     | 12.604       | 0           | 7.344.102  | 0          |
| Satena · Elevación (m)         | 57          | 422,07       | 170         | 2.975      | 2          |

En ambos CSV el promedio queda muy por encima de la mediana: pocos registros enormes jalan la media. En pasajeros, la mitad de las filas mueve 9 personas o menos (rutas regionales pequeñas), pero la ruta mayor llega a 79.817 en un solo mes (Avianca, Rionegro–Bogotá, enero de 2020). En carga, la mediana es 0 porque el 71 % de las filas no registra carga.

| **Texto**    | **Líneas** | **Palabras** | **Caracteres (con / sin espacios)** | **Top 5 palabras (sin conectores)**                        |
|--------------|------------|--------------|-------------------------------------|------------------------------------------------------------|
| juvenila.txt | 8.840      | 84.333       | 495.072 / 414.964                   | vida (193), dos (137), años (132), hombre (117), vez (113) |
| sample3.txt  | 21         | 546          | 3.521 / 2.991                       | natura, verum, potest, rebus, modo (3 c/u; empate)         |

Patrones tipo log: ninguno de los dos textos es un log. En juvenila.txt la palabra «error» aparece 4 veces, como palabra normal del texto, y hay 72 menciones de años (1800–2099); en sample3.txt no hay ninguna coincidencia.

## 3. Gráficos

### Transporte aéreo comercial (CSV)

![Pasajeros mensuales 2020–2022 (gráfico de líneas; se excluye octubre de 2025)](img/t_line.png)

*Pasajeros mensuales 2020–2022 (gráfico de líneas; se excluye octubre de 2025)**Gráfico de líneas: pasajeros mensuales 2020–2022 (se excluye octubre de 2025 por ser un solo mes).*

![Participación de pasajeros por tipo de tráfico (pastel)](img/t_pie.png)

*Participación de pasajeros por tipo de tráfico (pastel)*

![Pasajeros vs. carga, escala log (dispersión)](img/t_scatter.png)

*Pasajeros vs. carga, escala log (dispersión)*

### Aeropuertos Satena (CSV)

![Aeropuertos Satena: nacional vs. internacional (pastel)](img/s_pie.png)

*Aeropuertos Satena: nacional vs. internacional (pastel)*

![Elevación vs. temperatura (dispersión)](img/s_scatter.png)

*Elevación vs. temperatura (dispersión)*

### Textos (TXT)

![juvenila.txt: 10 palabras más frecuentes](img/juvenila_barh.png)

*juvenila.txt: 10 palabras más frecuentes*

![sample3.txt: 10 palabras más frecuentes](img/sample3_barh.png)

*sample3.txt: 10 palabras más frecuentes*

![juvenila.txt: longitud de líneas (histograma)](img/juvenila_hist.png)

*juvenila.txt: longitud de líneas (histograma)*

![sample3.txt: longitud de líneas (histograma)](img/sample3_hist.png)

*sample3.txt: longitud de líneas (histograma)*

## 4. Tres conclusiones a partir de los gráficos

**1. La pandemia casi borró el tráfico aéreo y la recuperación fue rápida.** De enero a abril de 2020 los pasajeros mensuales cayeron de 3,66 millones a 12.786 (−99,6 %). Hacia diciembre de 2021 ya se movían 4,06 millones, un 11 % más que en enero de 2020. Un detalle para verificar: de diciembre de 2021 a enero de 2022 la cifra baja 36 % y luego se mantiene plana en 2,2–2,7 millones, algo que el gráfico muestra pero los datos por sí solos no explican (podría ser cambio de metodología o duplicados entre aerolíneas).

**2. El mercado está muy concentrado, en rutas nacionales y en pocos nodos.** El 71,2 % de los pasajeros viaja en tráfico N y el 28,1 % en I, y el 85 % tiene destino Colombia. Avianca suma el 40 % de los pasajeros y, con Aires, casi el 62 %. Bogotá y Rionegro concentran al menos el 43,5 % de los pasajeros como origen. La mediana de 9 pasajeros por fila confirma que, aparte de esos nodos, hay una larga cola de rutas pequeñas.

**3. Pasajeros y carga se relacionan solo cuando se mira la escala correcta; y la geografía de Satena se refleja en los datos.** En el diagrama de dispersión, la correlación lineal entre pasajeros y carga es casi nula (0,08), porque unos pocos vuelos de carga distorsionan todo; en escala logarítmica, sobre las 32.909 filas con ambos valores, sube a 0,72. En Satena, el 84 % de los 57 aeropuertos son nacionales y la mayoría está a baja altura (la mitad por debajo de 170 m, frente a los 2.548 m de El Dorado); entre los 37 con temperatura registrada, a más elevación menos calor (correlación −0,80), aunque el 35 % de las temperaturas falta, lo que limita esa lectura.

### Observaciones sobre los textos

- juvenila.txt: las palabras más repetidas (vida, años, hombre, tiempo, espíritu) reflejan el tono reflexivo y autobiográfico de la obra. El histograma muestra que el 89 % de las líneas mide entre 60 y 79 caracteres: es el ancho fijo de formato de Gutenberg, no una característica del autor.

- sample3.txt: sus líneas son párrafos largos (promedio de 220 caracteres, máximo 818) y solo 3 líneas son cortas (títulos). Con apenas 546 palabras, el top 5 es un empate en 3 repeticiones, así que no hay una palabra dominante como en un texto real.

*Herramientas: Python (pandas y matplotlib). Los conectores excluidos del top de palabras corresponden a listas de palabras vacías en español y latín.*
