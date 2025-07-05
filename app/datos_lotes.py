import csv
import os
from app.modelo import Lote, Receta

def guardar_lote_csv(lote):
    ruta = "data/lotes.csv"
    archivo_nuevo = not os.path.exists(ruta)

    with open(ruta, "a", newline="", encoding="utf-8") as csvfile:
        campos = [
            "nombre_receta", "litros_objetivo",
            "fecha", "densidad_inicial", "densidad_final", "litros_embotellados"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=campos)

        if archivo_nuevo:
            writer.writeheader()

        writer.writerow({
            "nombre_receta": lote.receta.nombre,
            "litros_objetivo": lote.receta.litros_objetivo,
            "fecha": lote.fecha,
            "densidad_inicial": lote.densidad_inicial,
            "densidad_final": lote.densidad_final,
            "litros_embotellados": lote.litros_embotellados
        })

def cargar_lotes_csv():
    lotes = []
    try:
        with open("data/lotes.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                nombre_receta = row["nombre_receta"]
                litros_objetivo = float(row["litros_objetivo"])
                fecha = row["fecha"]
                densidad_inicial = float(row["densidad_inicial"])
                densidad_final = float(row["densidad_final"])
                litros_embotellados = float(row["litros_embotellados"])

                receta = Receta(nombre_receta, litros_objetivo)
                lote = Lote(receta, fecha, densidad_inicial, densidad_final, litros_embotellados)
                lotes.append(lote)
    except FileNotFoundError:
        pass  # Si no existe aún el archivo, devuelve lista vacía
    return lotes
