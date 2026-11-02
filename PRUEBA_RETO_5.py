# Reto #5 --- Alejandro Arcila Rua ---- Gabriela Galindo Herrera.
# Consola CLI para analisis y visualización de archivos reales.

#No hay patrones log ni conectores en ingles debido a la naturaleza de los archivos seleccionados para la ejecución del codigo.
#Gran cantidad de los # (hashtag) son con la intención de recordar la utilidad de las funciones/DEF para la sustentación con Henry

import csv
import os
import re
import statistics
from collections import Counter
from datetime import datetime

import matplotlib.pyplot as plt

CARPETA_GRAFICOS = "graficos"

#-------Funciones de 3° grado------- (Funcionan para no reiterar sobre el mismo procedimiento en multiples menus)

def pedir_entero(mensaje, minimo, maximo):  #Pide un entero en [minimo, maximo] hasta que sea válido.
    while True:
        valor = input(mensaje).strip()
        try:
            n = int(valor)
            if minimo <= n <= maximo:
                return n
            print(f"  Ingresa un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  Entrada inválida: escribe un número entero.")


def pedir_archivo(extensiones, mensaje):  #Pide una ruta del archivo y valida que exista y tenga la extensión correcta dicho archivo
    ruta = input(mensaje).strip().strip('"').strip("'")
    if not ruta:
        print("  No ingresaste ninguna ruta.")
        return None
    if not os.path.isfile(ruta):
        print(f"  El archivo '{ruta}' no existe.")
        return None
    if not ruta.lower().endswith(extensiones):
        print(f"  El archivo debe terminar en {extensiones}.")
        return None
    return ruta


def mostrar_grafico(nombre):    #Guarda el gráfico actual como PNG y lo muestra.
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)
    ruta = os.path.join(CARPETA_GRAFICOS, nombre)
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    print(f"  Gráfico guardado en: {ruta}")
    plt.show()
    plt.close()


def leer_texto(ruta):       #Lee un archivo de texto probando varias codificaciones para evitar que el sistema crashee.
    for cod in ("utf-8", "latin-1"):
        try:
            with open(ruta, "r", encoding=cod) as f:
                return f.readlines()
        except UnicodeDecodeError:
            continue
        except OSError as e:
            print(f"  No se pudo leer el archivo: {e}")
            return None
    return None

#-------Funciones de 2° grado-------

def explorar_directorio():              #Es la función esencial para la ejecución del menu principal.
    ruta = input("Ruta del directorio (Enter = carpeta actual): ").strip() or "."
    if not os.path.isdir(ruta):
        print(f"  '{ruta}' no es un directorio válido.")
        return
    try:
        archivos = sorted(
            f for f in os.listdir(ruta) if f.lower().endswith((".txt", ".csv"))
        )
    except PermissionError:
        print("  No tienes permisos para leer ese directorio.")
        return

    if not archivos:
        print("  No se encontraron archivos .txt ni .csv.")
        return
    print(f"\n  Archivos encontrados en '{ruta}':")
    for i, nombre in enumerate(archivos, 1):
        kb = os.path.getsize(os.path.join(ruta, nombre)) / 1024
        print(f"  {i:>2}. {nombre:<40} {kb:>9.1f} KB")

#-------Funciones de 2° grado relacionadas con .txt-------

def palabras_de(lineas):
    texto = " ".join(lineas).lower()
    return re.findall(r"[a-záéíóúüñ]+", texto)


CONECTORES = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "al",
    "y", "e", "o", "u", "que", "en", "a", "por", "para", "con", "sin", "se",
    "su", "sus", "lo", "le", "les", "es", "son", "fue", "como", "pero", "mas",
    "más", "si", "sí", "no", "ni", "ya", "me", "mi", "te", "tu", "nos", "este",
    "esta", "esto", "ese", "esa", "eso", "muy", "hay", "ha", "han", "había",
    "sobre", "entre", "cuando", "donde", "porque", "también", "todo", "todos","The","the"
}

def top_palabras(lineas, n):
    palabras = [p for p in palabras_de(lineas) if p not in CONECTORES and len(p) > 2]
    return Counter(palabras).most_common(n)


def resumen_texto(lineas):        #Importante para el funcionamiento de la opcion 1 del submenu
    texto = "".join(lineas)
    total_palabras = len(texto.split())
    con_espacios = len(texto)
    sin_espacios = len(re.sub(r"\s", "", texto))

    print("-------RESUMEN ESTADÍSTICO-------")
    print(f"""
    Líneas totales:               {len(lineas)}
    Palabras totales:             {total_palabras}
    Caracteres (con espacios):    {con_espacios}
    Caracteres (sin espacios):    {sin_espacios}
    """)

    print("\n  Top 5 palabras más repetidas (sin conectores):")
    for i, (pal, cant) in enumerate(top_palabras(lineas, 5), 1):
        print(f"    {i}. {pal:<15} {cant}")


def grafico_palabras(lineas):
    top = top_palabras(lineas, 10)
    if not top:
        print("  No hay palabras suficientes para graficar.")
        return
    palabras = [p for p, _ in top][::-1]  # invertido: la más frecuente arriba
    cantidades = [c for _, c in top][::-1]
    plt.figure(figsize=(9, 5))
    plt.barh(palabras, cantidades, color="steelblue")
    plt.title("Top 10 palabras más frecuentes")
    plt.xlabel("Frecuencia")
    plt.ylabel("Palabra")
    mostrar_grafico("g1_frecuencia_palabras.png")


def grafico_longitud_lineas(lineas):
    longitudes = [len(l.rstrip("\n")) for l in lineas]
    if not longitudes:
        print("  El archivo está vacío.")
        return
    maximo = max(longitudes)
    limites = list(range(0, maximo + 51, 50))
    if len(limites) < 2:
        limites = [0, 50]
    plt.figure(figsize=(9, 5))
    plt.hist(longitudes, bins=limites, color="seagreen", edgecolor="black")
    plt.title("Distribución de longitud de líneas")
    plt.xlabel("Caracteres por línea (rangos de 50)")
    plt.ylabel("Cantidad de líneas")
    plt.xticks(limites[:: max(1, len(limites) // 12)])
    mostrar_grafico("g2_longitud_lineas.png")


def menu_textos():
    ruta = pedir_archivo((".txt",), "Ruta del archivo .txt: ")
    if not ruta:
        return
    lineas = leer_texto(ruta)
    if lineas is None:
        return
    if not lineas:
        print("  El archivo está vacío.")
        return
    print(f"  Archivo cargado: {ruta} ({len(lineas)} líneas)")

    while True:
        print("\n--- SUBMENÚ TEXTOS ---")
        print("""
        1. Resumen estadístico
        2. Extracción de patrones (logs)
        3. Grafico -> Barh
        4. Grafico -> hist (historico)
        5. Volver
        """)

        op = pedir_entero("Opción: ", 1, 5)
        if op == 1:
            resumen_texto(lineas)
        elif op == 2:
            print("No se usaron archivos tipo LOG para el ejemplo")
        elif op == 3:
            grafico_palabras(lineas)
        elif op == 4:
            grafico_longitud_lineas(lineas)
        else:
            break

#-------Funciones de 2° grado relacionadas con archivos .csv-------

def a_numero(valor):    #Convierte texto a float; previniendo errores
    if valor is None:
        return None
    v = valor.strip().replace(" ", "")
    if v == "" or v.lower() in ("nan", "null", "none", "na", "n/a", "-"):
        return None
    if "," in v and "." not in v:
        v = v.replace(",", ".")
    else:
        v = v.replace(",", "")
    try:
        return float(v)
    except ValueError:
        return None


def a_fecha(valor):
    for dato in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(valor.strip(), dato)
        except (ValueError, AttributeError):
            continue
    return None


def cargar_csv(ruta):
    for cod in ("utf-8-sig", "latin-1"):
        try:
            with open(ruta, "r", encoding=cod, newline="") as f:
                muestra = f.read(4096)
                f.seek(0)
                try:
                    dialecto = csv.Sniffer().sniff(muestra, delimiters=",;\t|")
                except csv.Error:
                    dialecto = csv.excel
                lector = csv.DictReader(f, dialect=dialecto)
                columnas = lector.fieldnames
                filas = list(lector)
            if not columnas or not filas:
                print("  El CSV está vacío o no tiene encabezados.")
                return None, None
            return columnas, filas
        except UnicodeDecodeError:
            continue
        except (OSError, csv.Error) as e:
            print(f"  Error al leer el CSV: {e}")
            return None, None
    return None, None


def elegir_columna(columnas, mensaje):
    for i, c in enumerate(columnas, 1):
        print(f"    {i}. {c}")
    n = pedir_entero(mensaje, 1, len(columnas))
    return columnas[n - 1]


def columna_numerica(filas, col):
    return [n for n in (a_numero(f.get(col)) for f in filas) if n is not None]


def vista_previa(columnas, filas):
    def imprimir(subset, inicio):
        for i, fila in enumerate(subset, inicio):
            print(f"  {i:>4} | " + " | ".join(str(fila.get(c, ""))[:14] for c in columnas))

    print("-------")
    print(f"VISTA PREVIA  ({len(filas)} filas, {len(columnas)} columnas)")
    print("-------")
    print("  " + " " * 4 + " | " + " | ".join(c[:14] for c in columnas))
    print("\n  Primeras 10 filas:")
    imprimir(filas[:10], 1)
    print("\n  Últimas 5 filas:")
    imprimir(filas[-5:], max(1, len(filas) - 4))


def estadisticas(columnas, filas):
    col = elegir_columna(columnas, "  Columna numérica: ")
    valores = columna_numerica(filas, col)
    if not valores:
        print(f"  La columna '{col}' no tiene valores numéricos válidos.")
        return
    descartados = len(filas) - len(valores)
    print("-------")
    print(f"""ESTADÍSTICAS DE '{col}'
    Registros válidos: {len(valores)}  (descartados: {descartados})
    Promedio:          {statistics.mean(valores):.2f}
    Mediana:           {statistics.median(valores):.2f}
    Máximo:            {max(valores):.2f}
    Mínimo:            {min(valores):.2f}
    """)

def grafico_tendencia(columnas, filas):
    print("  Columna del eje X (fechas o categorías ordenadas):")
    cx = elegir_columna(columnas, "  X: ")
    print("  Columna del eje Y (numérica):")
    cy = elegir_columna(columnas, "  Y: ")

    pares = []
    for f in filas:
        y = a_numero(f.get(cy))
        x_txt = (f.get(cx) or "").strip()
        if y is not None and x_txt:
            pares.append((x_txt, y))
    if len(pares) < 2:
        print("  No hay suficientes datos válidos para graficar.")
        return

    fechas = [a_fecha(x) for x, _ in pares]
    if all(fechas):
        datos = sorted(zip(fechas, [y for _, y in pares]))
        xs, ys = [d[0] for d in datos], [d[1] for d in datos]
        es_fecha = True
    else:
        xs, ys = [x for x, _ in pares], [y for _, y in pares]
        es_fecha = False

    plt.figure(figsize=(10, 5))
    plt.plot(xs, ys, marker="o", markersize=3, color="darkorange")
    plt.title(f"Evolución de {cy} según {cx}")
    plt.xlabel(cx)
    plt.ylabel(cy)
    plt.grid(True, alpha=0.3)
    if es_fecha:
        plt.gcf().autofmt_xdate()
    else:
        paso = max(1, len(xs) // 15)
        plt.xticks(range(0, len(xs), paso), xs[::paso], rotation=45, ha="right")
    mostrar_grafico("g3_tendencia.png")


def grafico_pastel(columnas, filas):
    col = elegir_columna(columnas, "  Columna categórica: ")
    cats = [(f.get(col) or "").strip() for f in filas]
    cats = [c for c in cats if c]
    if not cats:
        print("  La columna no tiene datos.")
        return
    conteo = Counter(cats)
    if len(conteo) > 8:
        principales = conteo.most_common(7)
        otros = sum(conteo.values()) - sum(c for _, c in principales)
        etiquetas = [k for k, _ in principales] + ["Otros"]
        valores = [v for _, v in principales] + [otros]
        print(f"  ({len(conteo)} categorías: se muestran las 7 principales + 'Otros')")
    else:
        etiquetas, valores = list(conteo.keys()), list(conteo.values())

    plt.figure(figsize=(8, 8))
    plt.pie(valores, labels=etiquetas, autopct="%1.1f%%", startangle=90)
    plt.title(f"Participación por {col}")
    mostrar_grafico("g4_pastel.png")


def grafico_dispersion(columnas, filas):
    print("  Primera variable numérica:")
    cx = elegir_columna(columnas, "  X: ")
    print("  Segunda variable numérica:")
    cy = elegir_columna(columnas, "  Y: ")

    xs, ys = [], []
    for f in filas:
        x, y = a_numero(f.get(cx)), a_numero(f.get(cy))
        if x is not None and y is not None:
            xs.append(x)
            ys.append(y)
    if len(xs) < 2:
        print("  No hay suficientes pares numéricos válidos.")
        return

    plt.figure(figsize=(8, 6))
    plt.scatter(xs, ys, alpha=0.6, color="purple")
    plt.title(f"Relación entre {cx} y {cy}")
    plt.xlabel(cx)
    plt.ylabel(cy)
    plt.grid(True, alpha=0.3)
    try:
        r = statistics.correlation(xs, ys)
        print(f"  Coeficiente de correlación de Pearson: {r:.3f}")
    except (statistics.StatisticsError, AttributeError):
        pass
    mostrar_grafico("g5_dispersion.png")


def menu_csv():
    ruta = pedir_archivo((".csv",), "Ruta del archivo .csv: ")
    if not ruta:
        return
    columnas, filas = cargar_csv(ruta)
    if columnas is None:
        return
    print(f"  Archivo cargado: {ruta} ({len(filas)} filas, {len(columnas)} columnas)")

    while True:
        print("\n--- SUBMENÚ CSV ---")
        print("""
        1. Vista previa de datos
        2. Estadisticas descriptivas"
        3. Grafico -> Plot
        4. Grafico -> Pie
        5. Grafico -> Scatter
        6. Volver
        """)
        op = pedir_entero("Opción: ", 1, 6)
        if op == 1:
            vista_previa(columnas, filas)
        elif op == 2:
            estadisticas(columnas, filas)
        elif op == 3:
            grafico_tendencia(columnas, filas)
        elif op == 4:
            grafico_pastel(columnas, filas)
        elif op == 5:
            grafico_dispersion(columnas, filas)
        else:
            break

#----FUNCION PRINCIPAL (BLOQUE CODIGO ESCENCIAL)

def main():
    while True:
        print()
        print("-------EXPLORADOR CLI DE DATOS REALES-------")   
        print("""
        1. Explorar directorio
        2. Procesar bitacoras / textos (Archivos .txt)
        3. Analizar dataset de datos abiertos (.csv)
        4. Salir
        """)
        op = pedir_entero("Opción: ", 1, 4)
        try:
            if op == 1:
                explorar_directorio()
            elif op == 2:
                menu_textos()
            elif op == 3:
                menu_csv()
            else:
                print("¡Hasta pronto!")
                break
        except KeyboardInterrupt:
            print("\n  Operación cancelada.")
        except Exception as e:  # red de seguridad para que la app no se caiga
            print(f"  Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    main()