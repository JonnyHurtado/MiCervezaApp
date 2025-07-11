import csv
from app.modelo import Ingrediente

ARCHIVO_INGREDIENTES = "ingredientes.csv"


def guardar_ingredientes(inventario):
    with open("data/ingredientes.csv", "w", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["nombre", "tipo", "unidad", "stock", "precio_unitario"])
        for ing in inventario:
            escritor.writerow([
                ing.nombre, ing.tipo, ing.unidad, ing.stock, ing.precio_unitario
            ])

def cargar_ingredientes():
    ingredientes = []
    with open("data/ingredientes.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ing = Ingrediente(
                row["nombre"],
                row["tipo"],
                row["unidad"],
                float(row["stock"]),
                float(row["precio_unitario"])
            )
            ingredientes.append(ing)
    return ingredientes

import csv
import os

def guardar_receta_en_csv(receta):
    ruta = "data/recetas.csv"
    archivo_nuevo = not os.path.exists(ruta)

    with open(ruta, "a", newline="", encoding="utf-8") as csvfile:
        campos = ["nombre", "litros_objetivo", "ingrediente", "cantidad", "tipo", "precio_unitario"]
        writer = csv.DictWriter(csvfile, fieldnames=campos)

        if archivo_nuevo:
            writer.writeheader()

        for ing, cant in receta.ingredientes:
            writer.writerow({
                "nombre": receta.nombre,
                "litros_objetivo": receta.litros_objetivo,
                "ingrediente": ing.nombre,
                "cantidad": cant,
                "tipo": ing.tipo,
                "precio_unitario": ing.precio_unitario
            })
