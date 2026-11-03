# Documento de analisis

## 1. Origen y qué representa cada archivo

| **Archivo**                    | **Origen**                                                       | **Qué representa**                                                                                                                                                                                                                                                                         | **Tamaño**                    |
|--------------------------------|------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| Aeropuertos_Satena_2026.csv    | Portal Nacional de Datos Abiertos (Datos.gov.co)                 | Catálogo de aeropuertos que atiende Satena: nombre, ciudad, departamento, tipo de operación (nacional/internacional), códigos OACI e IATA, elevación, temperatura y coordenadas. Es un directorio de infraestructura, sin fechas ni series de tiempo.                                      | 57 filas × 12 columnas        |
| Transporte_Aéreo_Comercial.csv | Portal Nacional de Datos Abiertos (Datos.gov.co)                 | Estadística mensual de vuelos comerciales: cada fila es una ruta origen–destino operada por una aerolínea en un mes, con tipo de tráfico (N/I/E), tipo de vuelo, pasajeros y kilos de carga y correo. Cubre enero–diciembre de 2020, 2021 y 2022, 2023, 2024, 2025 hasta agosto del 2026 . | 478.011 filas × 16 columnas   |
| juvenila.txt                   | Biblioteca de dominio público                                    | «Juvenilia; Prosa ligera», de Miguel Cané, en español: prosa literaria del siglo XIX.                                                                                                                                                                                                      | 8.840 líneas, 84.333 palabras |
| sample3.txt                    | Generado aleatoriamente                                          | Texto de relleno en seudo-latín sin significado real.                                                                                                                                                                                                                                      | 21 líneas, 546 palabras       |

---
## 2. Tres conclusiones a partir de los gráficos

**1. La pandemia casi borró el tráfico aéreo y la recuperación fue rápida.** De enero a abril de 2020 los pasajeros mensuales cayeron de 3,66 millones a 12.786 (−99,6 %). Hacia diciembre de 2021 ya se movían 4,06 millones, un 11 % más que en enero de 2020. Un detalle para verificar: de diciembre de 2021 a enero de 2022 la cifra baja 36 % y luego se mantiene plana en 2,2–2,7 millones, algo que el gráfico muestra pero los datos por sí solos no explican (podría ser cambio de metodología o duplicados entre aerolíneas).

**2. El mercado está muy concentrado, en rutas nacionales y en pocos nodos.** El 71,2 % de los pasajeros viaja en tráfico N y el 28,1 % en I, y el 85 % tiene destino Colombia. Avianca suma el 40 % de los pasajeros y, con Aires, casi el 62 %. Bogotá y Rionegro concentran al menos el 43,5 % de los pasajeros como origen. La mediana de 9 pasajeros por fila confirma que, aparte de esos nodos, hay una larga cola de rutas pequeñas.

**3. Pasajeros y carga se relacionan solo cuando se mira la escala correcta; y la geografía de Satena se refleja en los datos.** En el diagrama de dispersión, la correlación lineal entre pasajeros y carga es casi nula (0,08), porque unos pocos vuelos de carga distorsionan todo; en escala logarítmica, sobre las 32.909 filas con ambos valores, sube a 0,72. En Satena, el 84 % de los 57 aeropuertos son nacionales y la mayoría está a baja altura (la mitad por debajo de 170 m, frente a los 2.548 m de El Dorado); entre los 37 con temperatura registrada, a más elevación menos calor (correlación −0,80), aunque el 35 % de las temperaturas falta, lo que limita esa lectura.


### Video de sustentacion:
https://youtu.be/xlWe3LZKy74


